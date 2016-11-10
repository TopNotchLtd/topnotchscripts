import sys
import win32api
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-e", "--exclude", action="store", type="string", dest="exclude", default="none", help="browser to exclude. Valid entries are: ie10, ie11, edge, firefox, chrome, none")
(options, args) = parser.parse_args()
excludedBrowser = options.exclude;

if excludedBrowser != "ie10":
	win32api.WinExec("C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun start \"I:\VMs\Windows 8.vmwarevm\Windows 8.vmx\"")

if excludedBrowser != "ie11":
	win32api.WinExec("C:\\Program Files\\Internet Explorer\\iexplore")

if excludedBrowser != "edge":
	win32api.WinExec("explorer microsoft-edge://")

if excludedBrowser != "firefox":
	win32api.WinExec("C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe")

if excludedBrowser != "chrome":
	win32api.WinExec("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")