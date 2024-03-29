#!/usr/bin/python2.7

from __future__ import print_function

import argparse
import email
import os
import shutil
import smtplib
import subprocess
import sys

import lxml.html
import requests
import StringIO
import urlparse

USI = 'https://updates.software-univention.de/download/scripts/univention-support-info'
USI_SCRIPT = '/usr/share/univention-support-info/usi.py'

UPLOAD = 'https://upload.univention.de/'


class Main(object):

	def __init__(self, args):
		self.args = args

	def execute(self):
		self.download_script()
		return self.run_script()

	def download_script(self):
		try:
			os.makedirs('/usr/share/univention-support-info')
		except EnvironmentError:
			pass
		try:
			etag = None
			with open('/usr/share/univention-support-info/.etag') as fd:
				etag = fd.read().strip()
		except EnvironmentError:
			pass

		headers = {}
		if etag:
			headers['If-None-Match'] = etag
		response = requests.get(USI, headers=headers)
		if response.status_code == 200:
			with open(USI_SCRIPT, 'wb') as fd:
				fd.write(response.content)
			os.chmod(USI_SCRIPT, 0o755)
			etag = response.headers.get('ETag')
			if etag:
				with open('/usr/share/univention-support-info/.etag', 'w') as fd:
					fd.write(etag)
			print('Collected new Univention Support Info', file=sys.stderr)
		elif response.status_code != 304:
			print('Failed to download USI script. Trying to use cached one!', file=sys.stderr)
		else:
			print('Using cached Univention Support Info', file=sys.stderr)

	def run_script(self):
		ceep = True
		keep = self.args.keep
		cmd = [USI_SCRIPT]
		if self.args.encrypt:
			cmd.append('--encrypt')
		if self.args.debug:
			cmd.append('--debug')
		if not self.args.quite:
			cmd.append('--verbose')
		print('Starting Univention Support Info...', file=sys.stderr)
		sys.stderr.flush()

		output = ""
		process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=sys.stderr)
		while True:
			pout = process.stdout.readline()
			if pout == '' and process.poll() is not None:
				break
			if pout:
				if not self.args.quite:
					sys.stderr.write(pout)
					sys.stderr.flush()
				output += pout
		returncode = process.poll()
		archives = []
		output = output.splitlines()
		for i, line in enumerate(output):
			if 'univention-support-info-' in line:
				archives.append(line.split()[-1])
		if not archives:
			print('No archive could be created!', file=sys.stderr)
			return 1
		# print('Univention Support Info created %r.' % (archives,), file=sys.stderr)

		# returncode = 0
		try:
			if self.args.folder:
				print('Copying archives to %s...' % (self.args.folder,), file=sys.stderr)
				for archive in archives:
					try:
						target = os.path.join(self.args.folder, os.path.basename(archive))
						shutil.copyfile(archive, target)
						os.chmod(target, 0o600)
						ceep = False
					except BaseException as exc:
						print('Could not copy a backup of the archives: %s' % (exc,), file=sys.stderr)
						returncode = 1

			if self.args.upload_to_univention:
				print('Uploading archive to Univention...', file=sys.stderr)
				try:
					archive = archives[0]  # will be the encrypted one
					archive_id = self.upload_archive(archive)
				except BaseException as exc:
					print('Could not upload archive: %s' % (exc,), file=sys.stderr)
					keep = True
					return 1

				print('Archive has been uploaded with ID %s' % (archive_id,), file=sys.stderr)

				if self.args.sender and '@' in self.args.sender:
					print('Sending mail to Univention...', file=sys.stderr)
					try:
						self.send_mail(archive_id)
					except BaseException as exc:
						print('The mail could not be send: %s' % (exc,), file=sys.stderr)
						returncode = 1
			else:
				keep = True

		finally:
			if not keep and ceep:
				for archive in archives:
					os.remove(archive)

		return returncode

	def upload_archive(self, archive):
		response = requests.get(UPLOAD)
		html = StringIO.StringIO(response.text)
		tree = lxml.html.parse(html)
		form = tree.getroot().xpath('//form[@enctype="multipart/form-data"][@method="post"]')[0]
		upload_uri = urlparse.urljoin(UPLOAD, form.action)
		data = [(x.name, x.value) for x in form.xpath('//input') if x.type not in ('file', 'submit')]
		name = form.xpath('//input[@type="file"]')[0].name
		with open(archive) as fd:
			response = requests.post(upload_uri, files={name: fd}, data=data)
			return lxml.html.parse(StringIO.StringIO(response.text)).getroot().xpath('//div[@id="page-body"]/b')[0].text

	def send_mail(self, archive_id):
		subject = 'Univention System Info Upload'
		if self.args.ticket:
			subject = '[Ticket#%s] %s' % (self.args.ticket.strip('# abcdefghijklmnoprstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXZ'), subject)
		msg = email.MIMEText.MIMEText('''
		A new Univention system info archive has been uploaded.

		Archive ID: %s
		''' % (archive_id,))
		msg['Subject'] = subject
		msg['From'] = self.args.sender
		msg['To'] = self.args.recipient
		s = smtplib.SMTP()
		s.connect()
		s.sendmail(self.args.sender, [self.args.recipient], msg.as_string())


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--upload-to-univention', action='store_true', help='Uploads and sends the file via mail to Univention.')
	parser.add_argument('--sender', help='The mail address of the sender. If not given, no archive can be send to Univention.')
	parser.add_argument('--recipient', help='Recipient of the mail (by default %(default)s).', default='support@univention.de')
	parser.add_argument('--add-to-ticket', metavar='ticket', dest='ticket', help='Adds the file to the ticket number instead of creating a new one.')
	parser.add_argument('--copy-to-folder', metavar='folder', dest='folder', help='Copies a backup of the generated archives into the specified folder.')
	parser.add_argument('--encrypt', action='store_true', help='Encrypt the archive and send only the encrypted version to Univention')
	parser.add_argument('--keep', action='store_true', help='Don\'t delete the archive afterwards.', default=False)
	parser.add_argument('--quite', action='store_true', help='Almost no output', default=False)
	parser.add_argument('--debug', action='store_true', help='enable debug', default=False)
	args = parser.parse_args()
	if os.getuid() != 0:
		parser.error('Must be executed as root!')
	if args.folder and not os.path.isdir(args.folder):
		parser.error('Folder does not exists or is not a directory.')
	sys.exit(Main(args).execute())
