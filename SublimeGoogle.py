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
	"""
	Search selected text
	"""
	def google_search(self,text):
		"""
		Search text in google and place results in self.results, then show in quick panel
		"""
		sublime.status_message("Searching \""+text+"\" in google.")
		res = search.GoogleSearch(text)
		res.results_per_page=10
		self.results.append(["Open in browser", "http://google.com/search?q="+text])
		for x in res.get_results():
			self.results.append([x.title+": "+x.url, x.desc])
		sublime.status_message("Found "+str(res.num_results)+" results.")
		self.window.show_quick_panel(self.results, self.onResSelected)
		return 0
	def run(self):
		v = self.window.active_view()
		text = v.substr(v.sel()[0]).strip()
		self.results=list()
		self.google_search(text)

		return 0
	def onResSelected(self, num):
		"""
		Open page in browser
		"""
		if num == -1:
			return
		else:
			url = self.results[num][1]
			sublime.status_message("I\'ve opened web browser for this page.")
			webbrowser.open(url)
			return 1

class GoogleSearchInputCommand(GoogleSearchSelectionCommand):
	"""
	Search user's input
	"""
	def run(self):
		self.results=list()
		self.window.show_input_panel("Google search:", '', self.google_search, None, None)

		return 0
