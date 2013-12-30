#!/usr/bin/env python
#encoding:utf-8

from sgmllib import SGMLParser

class URLLister(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.is_a = False 
		self.is_p = False 
		self.name = []
		self.page = []

	def start_a(self, attrs):
		self.is_a = True 

	def end_a(self):
		self.is_a = False 

	def start_p(self, attrs):
		self.is_p = True 

	def end_p(self):
		self.is_p = False 
		
	def handle_data(self, text):
		if self.is_a:
			self.name.append(text)
		if self.is_p:
			self.page.append(text)

data = '''<tr>
<td height="207" colspan="2" align="left" valign="top" class="normal">
<p>Damien Rice - 《0》 </p>
<a href="http://galeki.xy568.net/music/Delicate.mp3">1. Delicate</a><br />
<a href="http://galeki.xy568.net/music/Volcano.mp3">2. Volcano</a><br />
<a href="http://galeki.xy568.net/music/The Blower's Daughter.mp3">3. The Blower's Daughter</a><br />
<a href="http://galeki.xy568.net/music/Cannonball.mp3">4. Cannonball </a><br />
<a href="http://galeki.xy568.net/music/Older Chests.mp3">5. Order Chests</a><br />
<a href="http://galeki.xy568.net/music/Amie.mp3">6. Amie</a><br />
<a href="http://galeki.xy568.net/music/Cheers Darlin'.mp3">7. Cheers Darling</a><br />
<a href="http://galeki.xy568.net/music/Cold Water.mp3">8. Cold water</a><br />
<a href="http://galeki.xy568.net/music/I Remember.mp3">9. I remember</a><br />
<a href="http://galeki.xy568.net/music/Eskimo.mp3">10. Eskimo</a></p>
</td>
</tr>'''

lister = URLLister()
lister.feed(data)

print lister.name
print lister.page
