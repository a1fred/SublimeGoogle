import sublime, sublime_plugin
try:
  import json
except ImportError:
  import simplejson as json
 
import urllib, urllib2
import os.path
import webbrowser
import search

class GoogleSearchSelectionCommand(sublime_plugin.WindowCommand):
	def run(self):
		v = self.window.active_view()
		text = v.substr(v.sel()[0]).strip()
		self.results=list()
		sublime.status_message("Searching \""+text+"\" in google.")
		res = search.GoogleSearch(text)
		res.results_per_page=10
		self.results.append(["Open in browser", "http://google.com/search?as_q="+text])
		for x in res.get_results():
			self.results.append([x.title+": "+x.url, x.desc])
		self.window.show_quick_panel(self.results, self.onResSelected)
		sublime.status_message("Found "+str(res.num_results())+"results.")
		return 0

	def onResSelected(self, num):
		if num == -1:
			return
		else:
			url = self.results[num][1]
			sublime.status_message("I\'ve opened web browser for this page.")
			webbrowser.open(url)
			return 1
