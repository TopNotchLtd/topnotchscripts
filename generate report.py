import csv
import sys
import smtplib
import datetime
import os.path

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from optparse import OptionParser

emailAddr = ""
password = ""
#Remove your address if you don't want to send emails to yourself
ccRecipients = "jake@topnotchltd.com, nolan@topnotchltd.com, billy@topnotchltd.com, daniel@topnotchltd.com, danny@topnotchltd.com, ivan@topnotchltd.com"

parser = OptionParser()
parser.add_option("-t", "--type", action="store", type="string", dest="type", default="txt", help="filetype to read from. Only valid values are 'csv' and 'txt'")
parser.add_option("-c", "--created", action="store", type="string", dest="created", help="filename of document to read created bugs from")
parser.add_option("-v", "--verified", action="store", type="string", dest="verified", help="filename of document to read verified bugs from")
parser.add_option("-r", "--rejected", action="store", type="string", dest="rejected", help="filename of document to read rejected bugs from")
parser.add_option("-b", "--browsers", action="store", type="string", dest="browsers", help="list of browsers tested, will be added as written")
parser.add_option("-d", "--devices", action="store", type="string", dest="devices", help="list of devices tested, will be added as written")
parser.add_option("-q", "--tablets", action="store", type="string", dest="tablets", help="list of tablets tested, will be added as written")
parser.add_option("-s", "--summary", action="store", type="string", dest="summary", help="summary of today's testing on this project")
parser.add_option("-n", "--nextsteps", action="store", type="string", dest="nextSteps", help="next steps for testing this project")
parser.add_option("-p", "--project", action="store", type="string", dest="project", help="name of project, for email subject line")
parser.add_option("-o", "--to", action="store", type="string", dest="to", help="recipient of email, can be multiple email addresses seperated by commas (,)")
parser.add_option("-u", "--url", action="store", type="string", dest="url", help="url for bug tracker (usually Jira), required if you pick CSV; must include trailing slash")
(options, args) = parser.parse_args()

if not options.to:
	parser.error("You must specifiy an email recipient (-o)")
if not options.project:
	parser.error("You must specifiy a project name (-p)")
if not options.summary:
	parser.error("You must include a summary (-s)")
if not options.nextSteps:
	parser.error("You must include next steps (-n)")
if options.type == "csv" and not options.url:
	parser.error("You must include url to bug tracker (-u) if using csv mode")

fileType = options.type
created = options.created
verified = options.verified
rejected = options.rejected
browsers = options.browsers
devices = options.devices
tablets = options.tablets
summary = options.summary
nextSteps = options.nextSteps
project = options.project
emailTo = options.to
trackerUrl = options.url

#Init lists
#These will become lists of lists if using CSV
lstCreated = []
lstVerified = []
lstRejected = []
now = datetime.datetime.now()

#Create functions
def ReadCsv(file):
	try:
		with open(created, 'rU') as infile:
			reader = csv.DictReader(infile)
			data = {}
			for row in reader:
				for header, value in row.items():
					try:
						data[header].append(value)
					except KeyError:
						data[header] = [value]

		newList = {"keys":[], "summaries":[]}
		newList["keys"] = data['Issue key']
		newList["summaries"] = data['Summary']
		return newList
	except:
		print "Error reading file " + file + "!"
		sys.exit()

def ReadTxt(file):
	try:
		newList = []
		f = open(file, 'r')
		newList = f.read().splitlines()
		return newList
	except:
		print "Error reading file " + file + "!"
		sys.exit()

#Returns a a dictionary
def BuildListText(list):
	output = {"text": "", "html": ""}

	if fileType == "txt":
		for c in list:	
			output["text"] += c + "\n"
			output["html"] += '<a href="' + c + '">' + c + "</a><br>"
	elif fileType == "csv":
		for j in range(0,len(list["keys"])):
			output["text"] += list["keys"][j] + " - " + list["summaries"][j]
			output["html"] += '<a href="' + trackerUrl + list["keys"][j] + '">' + list["keys"][j] + " - " + list["summaries"][j] + "</a><br>"

	return output;

#Read data from CSV file
if fileType == "csv":
	if created != None:
		lstCreated = ReadCsv(created)
	if verified != None:
		lstVerified = ReadCsv(verified)
	if rejected != None:
		lstRejected = ReadCsv(rejected)

elif fileType == "txt":
	if created != None:
		lstCreated = ReadTxt(created)

	if verified != None:
		lstVerified = ReadTxt(verified)

	if rejected != None:
		lstRejected = ReadTxt(rejected)
else:
	print "ERROR: Incorrect filetype specified"
	sys.exit()

print "Sending mail..."
#send email
msg = MIMEMultipart('alternative')
msg["Subject"] = str(now.month) + "/" + str(now.day) + "/" + str(now.year) + " QA Report - " + project
msg["From"] = emailAddr
msg["To"] = emailTo
msg["CC"] = ccRecipients

#Build the body of the email (text and html)
text = "QA Summary\n" + summary + "\n"
html = "<strong>QA Summary</strong><br>" + summary + "<br>"

if browsers != None:
	text += "Browsers Covered\n" + browsers + "\n"
	html += "<strong>Browsers Covered</strong><br>" + browsers + "<br>"

if devices != None:
	text += "Devices Covered\n" + devices + "\n"
	html += "<strong>Devices Covered</strong><br>" + devices + "<br>"

if tablets != None:
	text += "Tablets Covered\n" + tablets + "\n"
	html += "<strong>Tablets Covered</strong><br>" + tablets + "<br>"

if lstVerified:
	text += "Bugs/User Stories Verified\n"
	html += "<strong>Bugs/User Stories Verified</strong><br>"
	listText = BuildListText(lstVerified)
	text += listText["text"]
	html += listText["html"]

if lstRejected:
	text += "Bugs/User Stories Rejected\n"
	html += "<strong>Bugs/User Stories Rejected</strong><br>"
	listText = BuildListText(lstRejected)
	text += listText["text"]
	html += listText["html"]


if lstCreated:
	text += "Bugs/User Stories Created\n"
	html += "<strong>Bugs/User Stories Created</strong><br>"
	listText = BuildListText(lstCreated)
	text += listText["text"]
	html += listText["html"]


text += "Next Steps\n" + nextSteps
html += "<strong>Next Steps</strong><br>" + nextSteps

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

msg.attach(part1)
msg.attach(part2)

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(emailAddr, password)
server.sendmail(emailAddr, emailTo.split(",") + ccRecipients.split(","), msg.as_string())
server.quit()

print "Mail sent!"