#!/usr/bin/python2.7

import os
import sys
import shutil
import email
import smtplib
import argparse
import StringIO
import lxml.html
import urlparse
import subprocess

import requests

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
			print >> sys.stderr, 'Collected new Univention Support Info'
		elif response.status_code != 304:
			print >> sys.stderr, 'Failed to download USI script. Trying to use cached one!'
		else:
			print >> sys.stderr, 'Using cached Univention Support Info'

	def run_script(self):
		cmd = [USI_SCRIPT]
		if self.args.encrypt:
			cmd.append('--encrypt')
		print >> sys.stderr, 'Starting Univention Support Info...'
		sys.stderr.flush()
		process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=sys.stderr)
		stdout, _ = process.communicate()
		stdout = stdout.splitlines()
		archives = []
		for i, line in enumerate(stdout):
			if 'The encrypted data can be found here:' in line:
				archives.append(stdout[i + 1].strip())
			if 'The unencrypted data can be found here:' in line or 'The data can be found here:' in line:
				archives.append(stdout[i + 1].strip())
		if not archives:
			print >> sys.stderr, 'No archive could be created!'
			return 1
		print >> sys.stderr, 'Univention Support Info created %r.' % (archives,)

		returncode = 0
		try:
			if self.args.folder:
				print >> sys.stderr, 'Copying archives to %s...' % (self.args.folder,)
				for archive in archives:
					try:
						target = os.path.join(self.args.folder, os.path.basename(archive))
						shutil.copyfile(archive, target)
						os.chmod(target, 0o600)
					except BaseException as exc:
						print >> sys.stderr, 'Could not copy a backup of the archives: %s' % (exc,)
						returncode = 1

			if self.args.upload_to_univention:
				print >> sys.stderr, 'Uploading archive to Univention...'
				try:
					archive = archives[0]  # will be the encrypted one
					archive_id = self.upload_archive(archive)
				except BaseException as exc:
					print >> sys.stderr, 'Could not upload archive: %s' % (exc,)
					return 1

				print >> sys.stderr, 'Archive has been uploaded with ID %s' % (archive_id,)

				if self.args.sender and '@' in self.args.sender:
					print >> sys.stderr, 'Sending mail to Univention...'
					try:
						self.send_mail(archive_id)
					except BaseException as exc:
						print >> sys.stderr, 'The mail could not be send: %s' % (exc,)
						returncode = 1
		finally:
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
	parser.add_argument('--sender', help='The mail address of the sender. If not given, no archive will be send to Univention.')
	parser.add_argument('--recipient', help='Recipient of the mail (by default %(default)s).', default='feedback@univention.de')
	parser.add_argument('--add-to-ticket', metavar='ticket', dest='ticket', help='Adds the file to the ticket number instead of creating a new one.')
	parser.add_argument('--copy-to-folder', metavar='folder', dest='folder', help='Copies a backup of the generated archives into the specified folder.')
	parser.add_argument('--encrypt', action='store_true', help='Encrypt the archive and send only the encrypted version to Univention')
	args = parser.parse_args()
	if os.getuid() != 0:
		parser.error('Must be executed as root!')
	if args.folder and not os.path.isdir(args.folder):
		parser.error('Folder does not exists or is not a directory.')
	sys.exit(Main(args).execute())
