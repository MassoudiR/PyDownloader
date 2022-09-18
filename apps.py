from urllib.parse import urlparse
from urllib.request import urlopen
import youtube_dl
import re
import ast
import sys,json
import requests
from tiktok_downloader import ttdownloader , Snaptik
from bs4 import BeautifulSoup
from pytube import YouTube 
import TikTokApi
import asyncio
import instaloader
from vimeo_downloader import Vimeo
USERNAME = "paydownl"
PASSWORD = "pytube2022"
I = instaloader.Instaloader()



class Twitter():
	def __init__(self,video_url):
		video_id = video_url.split('/')[5].split('?')[0] if 's?=' in video_url else video_url.split('/')[5]
		self.log = {}
		sources = {
			"video_url" : "https://twitter.com/i/videos/tweet/"+video_id,
			"activation_ep" :'https://api.twitter.com/1.1/guest/activate.json',
			"api_ep" : "https://api.twitter.com/1.1/statuses/show.json?id="+video_id
		}
		headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0','accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-language' : 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5'}
		self.session = requests.Session()
		def send_request(self, url,method,headers):
			request = self.session.get(url, headers=headers) if method == "GET" else self.session.post(url, headers=headers)
			if request.status_code == 200:
				return request.text
			else:
				sys.exit("Bad request to {}, status code: {}.\nPlease sumbit an issue in the repo including this info.".format(url,request.status_code))
	
		token_request = send_request(self,sources["video_url"],"GET",headers)
		bearer_file = re.findall('src="(.*js)',token_request)
		file_content = send_request(self,str(bearer_file[0]),'GET',headers)
		bearer_token_pattern = re.compile('Bearer ([a-zA-Z0-9%-])+')
		bearer_token = bearer_token_pattern.search(file_content)
		headers['authorization'] = bearer_token.group(0)
		self.log['bearer'] = bearer_token.group(0)
		req2 = send_request(self,sources['activation_ep'],'post',headers)
		headers['x-guest-token'] = json.loads(req2)['guest_token']
		self.log['guest_token'] = json.loads(req2)['guest_token']
		# get link
		self.log['full_headers'] = headers
		api_request = send_request(self,sources["api_ep"],"GET",headers)

		try:
			js = json.loads(api_request)['extended_entities']['media'][0]['video_info']['variants']
			videos = js['video_info']['variants']
			self.img = js["media_url"]

			self.title= js["additional_media_info"]['title']
			print(js["additional_media_info"])
			print(js["additional_media_info"]['title'])

			self.log['vid_list'] = videos 
			self.videoQ={}
			for vid in videos:
				if vid['content_type'] == 'video/mp4':
						hq_video_url = vid['url']
						if "320x" in hq_video_url:
							self.videoQ["320p"] = hq_video_url
						elif "540x" in hq_video_url:
							self.videoQ["540p"] = hq_video_url
						elif "720x" in hq_video_url:
							self.videoQ["720p"] = hq_video_url
						else:
							pass


			print(self.videoQ)
					
		
		except:
			print("error")

class Download():
    def __init__( self , url:str ):
        self.url = url
        self.title : str 
        self.img = "/image/video.png"
        self.ln : any
        self.videoList = {}


        domain = urlparse(url).netloc
        if "youtu" in domain:
            self.YouTubeDownlowd()
        elif "insta" in domain:
            self.InstagramDownload()
        elif "facebook" in domain or "fb" in domain:
            if "fb.watch" in url:
                self.url = requests.get(url).url
            self.FaceBookDownlowd()
        elif "tiktok" in domain:
            self.TiktokDownload()
        elif "twitter" in domain:
            self.TwitterDownlowd()
        elif "linked" in domain:
            self.LinkedinDownload()
        elif "vimeo." in domain:
            self.VimeoDownload()
        else:
            self.WebDownload()
        
    def Get_Info(self):
        return (self.title ,self.img,0,self.videoList)

    def YouTubeDownlowd(self): 
        yt = YouTube(self.url)
        self.img = yt.thumbnail_url
        self.ln = yt.caption_tracks
        self.title = yt.title
        
        
        i = yt.streams.filter(progressive=True)
        
        for stream in i:
            res=stream
            qua = res.resolution
            link = yt.streams.get_by_itag(res.itag).url
            self.videoList[qua]=link
        
    def FaceBookDownlowd(self):
        soup = BeautifulSoup(urlopen(self.url),'html.parser')
        self.title = soup.title.get_text()
        self.img = "/image/video.png"
        print(self.url)
        try: 

            urlmobil = self.url.replace("www.","m.")
            soup = BeautifulSoup(urlopen(urlmobil),'html.parser')
            self.title = soup.find("meta", property="og:title")["content"]
            print(self.title)
            self.img = soup.find("meta", property="og:image")["content"]
            print(self.img)

        except: pass

        with youtube_dl.YoutubeDL() as ydl:
            url = ydl.extract_info(self.url, download=False)
            
            for x in (url['entries'][0]["formats"]):
                qua = x['format_id']
                if qua == "hd" or qua == "sd":
                    link = x['url']
                    self.videoList[qua]=link
            mp = url['entries'][0]["formats"][0]
            self.videoList["mp3"]= mp['url']
            
    def TwitterDownlowd(self):
        dl = Twitter(self.url)
        self.title = dl.title
        self.img = dl.img
        self.videoList = dl.videoQ

    def LinkedinDownload(self):
    
        page = requests.get( self.url )
        soup = BeautifulSoup(page.content, "html.parser")
        self.title = soup.find_all("title")[0].text

        videotag = soup.find_all("video")[0]
        self.img = videotag.get('data-poster-url')
        
        videourl = (ast.literal_eval((videotag.get('data-sources'))))[0]
        self.videoList = {'HD':videourl['src']}
    
    def TiktokDownload(self):

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        with TikTokApi.TikTokApi() as api:
            videox = api.video(url=self.url).info()
            
            self.title = videox['desc']
            print(self.title)
            self.img = videox['video']['originCover']
            print(self.img)

        #d=Snaptik(self.url)
       
            self.videoList={'Watermark':videox['video']['playAddr']}
        #self.videoList={'Watermark':videox['video']['playAddr'],"NoWatermark":d[0].json}

           
    def VimeoDownload(self):
        v = Vimeo(self.url)
        self.title = v.metadata.title
        self.img = v.metadata.thumbnail_large
        
        for x in v.streams:
            self.videoList[x.quality] = x.direct_url
            
    def InstagramDownload(self):
        try:
            I.login(USERNAME, PASSWORD)
        except:
            pass
        reg = "(?:https?:\/\/)?(?:www.)?instagram.com\/?([a-zA-Z0-9\.\_\-]+)?\/([p]+)?([reel]+)?([tv]+)?([stories]+)?\/([a-zA-Z0-9\-\_\.]+)\/?([0-9]+)?"
        posturl = re.findall(reg,self.url)[0][5]
        post = instaloader.Post.from_shortcode(I.context, posturl)
        if post.is_video :
            self.title = post.caption or post.title or post.profile
            self.img = post.url
            self.videoList={"HD" : post.video_url}
        else:
            self.title = post.caption or post.title or post.profile
            self.img = post.url
            self.videoList={"Photo" : post.url}

    def WebDownload(self):
        page = requests.get( self.url )
        soup = BeautifulSoup(page.content, "html.parser")
        getVideo = self.getVideoTag(soup)
        if getVideo :
            pass
        else:
            self.getIfremTag(soup)
                       
    def getVideoTag(self,soup):
        try :
            self.title = soup.find_all("title")[0].text
 
            videoTag = soup.find_all("video")[0]
         

            if videoTag:
                
                self.img = videoTag.get('poster') or 'image/video.png'
                video = videoTag.get('src')
                
                if video == None:
                    video = videoTag.find_all('source')[0].get('src')
                    try :
                        requests.get(video)
                    except:
                        if "http" not in video:
                            video = self.url+'/'+'..'+'/'+video
                            ##video = urlparse(url).netloc + '/' + video

                        

                self.videoList = {'HD':video}
            return True
        except:
            return None
        
    def getIfremTag(self,soup):
        ifrem = soup.find_all("iframe")
        for x in ifrem:
            link = x.get('src')
            domain = urlparse(link).netloc
            listUrlSupported = ["youtu","insta","vimeo","fb","facebbok","twitter","linked"]
            for urlsp in listUrlSupported:
                if urlsp in domain:
                    self.__init__(link)
                    break

            


