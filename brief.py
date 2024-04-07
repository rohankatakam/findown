from GoogleNews import GoogleNews
import re
import cohere
import json
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import numpy as np

## Environment variables
# Cohere initialization
api_key = "hlh0oA0Ac0fTZKDnEPa4KIeGGs3MApTYBPcZ7oa9"
co = cohere.Client(api_key)
# Source data
mbdf2 = [
    {'Source': 'MSNBC', 'Bias': 'Left', 'Agree': 26379, 'Disagree': 6853} , 
    {'Source': 'MTV News Online', 'Bias': 'Lean Left', 'Agree': 212, 'Disagree': 339} , 
    {'Source': 'Multiple Writers - Center', 'Bias': 'Center', 'Agree': 80, 'Disagree': 88} , 
    {'Source': 'Multiple Writers - Lean Left', 'Bias': 'Lean Left', 'Agree': 59, 'Disagree': 61} , 
    {'Source': 'Multiple Writers - Lean Right', 'Bias': 'Lean Right', 'Agree': 61, 'Disagree': 52} , 
    {'Source': 'Multiple Writers - Left', 'Bias': 'Left', 'Agree': 66, 'Disagree': 38} , 
    {'Source': 'Multiple Writers - Mixed', 'Bias': 'Mixed', 'Agree': 82, 'Disagree': 97} , 
    {'Source': 'Multiple Writers - Right', 'Bias': 'Right', 'Agree': 39, 'Disagree': 32} , 
    {'Source': 'Muscatine Journal', 'Bias': 'Center', 'Agree': 30, 'Disagree': 34} , 
    {'Source': 'My Central Jersey', 'Bias': 'Center', 'Agree': 11, 'Disagree': 16} , 
    {'Source': 'My Central Oregon', 'Bias': 'Center', 'Agree': 7, 'Disagree': 9} , 
    {'Source': 'My Colorado Springs News', 'Bias': 'Center', 'Agree': 10, 'Disagree': 12} , 
    {'Source': 'My High Plains KAMR', 'Bias': 'Center', 'Agree': 8, 'Disagree': 11} , 
    {'Source': 'My Panhandle News', 'Bias': 'Center', 'Agree': 9, 'Disagree': 11} , 
    {'Source': 'My Rye', 'Bias': 'Center', 'Agree': 6, 'Disagree': 7} , 
    {'Source': 'My Wabash Valley', 'Bias': 'Center', 'Agree': 15, 'Disagree': 13} , 
    {'Source': 'NAACP', 'Bias': 'Lean Left', 'Agree': 468, 'Disagree': 914} , 
    {'Source': 'Naples Daily News', 'Bias': 'Center', 'Agree': 19, 'Disagree': 24} , 
    {'Source': 'Nashville Post', 'Bias': 'Center', 'Agree': 11, 'Disagree': 13} , 
    {'Source': 'National Catholic Register', 'Bias': 'Right', 'Agree': 54, 'Disagree': 94} , 
    {'Source': 'National Committee to Preserve Social Security and Medicare', 'Bias': 'Left', 'Agree': 378, 'Disagree': 291} , 
    {'Source': 'National Conference of State Legislatures', 'Bias': 'Center', 'Agree': 33, 'Disagree': 33} , 
    {'Source': 'National Constitution Center', 'Bias': 'Center', 'Agree': 238, 'Disagree': 220} , 
    {'Source': 'National Federation of Independent Business', 'Bias': 'Lean Right', 'Agree': 55, 'Disagree': 65} , 
    {'Source': 'National Geographic', 'Bias': 'Center', 'Agree': 423, 'Disagree': 345} , 
    {'Source': 'National Institute for Civil Discourse', 'Bias': 'Center', 'Agree': 25, 'Disagree': 23} , 
    {'Source': 'National Interest', 'Bias': 'Center', 'Agree': 352, 'Disagree': 495} , 
    {'Source': 'National Journal', 'Bias': 'Center', 'Agree': 1107, 'Disagree': 871} , 
    {'Source': 'National Post', 'Bias': 'Lean Right', 'Agree': 358, 'Disagree': 160} , 
    {'Source': 'National Review (News)', 'Bias': 'Lean Right', 'Agree': 23746, 'Disagree': 10188} , 
    {'Source': 'National Review (Opinion)', 'Bias': 'Right', 'Agree': 564, 'Disagree': 366} , 
    {'Source': 'Nature.com', 'Bias': 'Center', 'Agree': 368, 'Disagree': 290} , 
    {'Source': 'Nautilus Quarterly', 'Bias': 'Center', 'Agree': 53, 'Disagree': 58} , 
    {'Source': 'NBC 10 Boston', 'Bias': 'Lean Left', 'Agree': 15, 'Disagree': 21} , 
    {'Source': 'NBC 12 WWBT', 'Bias': 'Center', 'Agree': 15, 'Disagree': 16} , 
    {'Source': 'NBC 15 WMTV', 'Bias': 'Center', 'Agree': 14, 'Disagree': 15} , 
    {'Source': 'NBC 29 WVIR', 'Bias': 'Center', 'Agree': 16, 'Disagree': 15} , 
    {'Source': 'NBC 4 WCMH', 'Bias': 'Center', 'Agree': 13, 'Disagree': 15} , 
    {'Source': 'NBC 5 Chicago', 'Bias': 'Center', 'Agree': 22, 'Disagree': 25} , 
    {'Source': 'NBC 5 Plattsburgh', 'Bias': 'Center', 'Agree': 7, 'Disagree': 6} , 
    {'Source': 'NBC 7 San Diego', 'Bias': 'Lean Left', 'Agree': 13, 'Disagree': 20} , 
    {'Source': 'NBC Connecticut', 'Bias': 'Lean Left', 'Agree': 15, 'Disagree': 20} , 
    {'Source': 'NBC News (Online)', 'Bias': 'Lean Left', 'Agree': 16319, 'Disagree': 15537} , 
    {'Source': 'NBC Today Show', 'Bias': 'Lean Left', 'Agree': 1776, 'Disagree': 1861} , 
    {'Source': 'Neal K. Katyal', 'Bias': 'Lean Left', 'Agree': 78, 'Disagree': 65} , 
    {'Source': 'NECN', 'Bias': 'Lean Right', 'Agree': 6, 'Disagree': 12} , 
    {'Source': 'Neil J. Young', 'Bias': 'Lean Left', 'Agree': 109, 'Disagree': 126} , 
    {'Source': 'Neil Patel', 'Bias': 'Right', 'Agree': 52, 'Disagree': 95} , 
    {'Source': 'Network for Responsible Public Policy', 'Bias': 'Center', 'Agree': 15, 'Disagree': 34} , 
    {'Source': 'Nevada Appeal', 'Bias': 'Center', 'Agree': 13, 'Disagree': 14} , 
    {'Source': 'Nevada Current', 'Bias': 'Center', 'Agree': 7, 'Disagree': 10} , 
    {'Source': 'New Discourses', 'Bias': 'Center', 'Agree': 199, 'Disagree': 214} , 
    {'Source': 'New Economy Working Group', 'Bias': 'Lean Left', 'Agree': 137, 'Disagree': 116} , 
    {'Source': 'New Hampshire Bulletin', 'Bias': 'Center', 'Agree': 5, 'Disagree': 8} , 
    {'Source': 'New Hampshire Public Radio', 'Bias': 'Center', 'Agree': 12, 'Disagree': 64} , 
    {'Source': 'New Hampshire Union Leader', 'Bias': 'Center', 'Agree': 119, 'Disagree': 136} , 
    {'Source': 'New Haven Register', 'Bias': 'Center', 'Agree': 18, 'Disagree': 19} , 
    {'Source': 'New Jersey Globe', 'Bias': 'Center', 'Agree': 47, 'Disagree': 54} , 
    {'Source': 'New Jersey Hills Media Group', 'Bias': 'Center', 'Agree': 10, 'Disagree': 10} , 
    {'Source': 'New Jersey Local News', 'Bias': 'Center', 'Agree': 9, 'Disagree': 12} , 
    {'Source': 'New Jersey Monitor', 'Bias': 'Lean Left', 'Agree': 38, 'Disagree': 39} , 
    {'Source': 'New Mexico In Depth', 'Bias': 'Center', 'Agree': 9, 'Disagree': 12} , 
    {'Source': 'New Orleans City Business', 'Bias': 'Center', 'Agree': 11, 'Disagree': 14} , 
    {'Source': 'New Pittsburgh', 'Bias': 'Left', 'Agree': 43, 'Disagree': 20} , 
    {'Source': 'New Republic', 'Bias': 'Left', 'Agree': 2272, 'Disagree': 984} , 
    {'Source': 'New Rockford Transcript', 'Bias': 'Center', 'Agree': 8, 'Disagree': 13} , 
    {'Source': 'New York Daily Gazette', 'Bias': 'Center', 'Agree': 8, 'Disagree': 10} , 
    {'Source': 'New York Daily News', 'Bias': 'Left', 'Agree': 1715, 'Disagree': 795} , 
    {'Source': 'New York Focus', 'Bias': 'Center', 'Agree': 10, 'Disagree': 15} , 
    {'Source': 'New York Magazine', 'Bias': 'Left', 'Agree': 2567, 'Disagree': 1128} , 
    {'Source': 'New York Post (News)', 'Bias': 'Lean Right', 'Agree': 19609, 'Disagree': 10537} , 
    {'Source': 'New York Post (Opinion)', 'Bias': 'Right', 'Agree': 541, 'Disagree': 289} , 
    {'Source': 'New York Times (News)', 'Bias': 'Lean Left', 'Agree': 35603, 'Disagree': 45984} , 
    {'Source': 'New York Times (Opinion)', 'Bias': 'Left', 'Agree': 21168, 'Disagree': 6439} , 
    {'Source': 'Newark Post', 'Bias': 'Center', 'Agree': 11, 'Disagree': 14} , 
    {'Source': 'News & Citizen', 'Bias': 'Center', 'Agree': 8, 'Disagree': 10} , 
    {'Source': 'News 12 Connecticut', 'Bias': 'Center', 'Agree': 18, 'Disagree': 14} , 
    {'Source': 'News 12 New Jersey', 'Bias': 'Center', 'Agree': 14, 'Disagree': 19} , 
    {'Source': 'News 4 Jax', 'Bias': 'Center', 'Agree': 16, 'Disagree': 21} , 
    {'Source': 'News 8000', 'Bias': 'Center', 'Agree': 11, 'Disagree': 11} , 
    {'Source': 'News 9 Oklahoma', 'Bias': 'Center', 'Agree': 13, 'Disagree': 10} , 
    {'Source': 'News Center Maine', 'Bias': 'Lean Left', 'Agree': 39, 'Disagree': 38} , 
    {'Source': 'News Channel 6 Wichita Falls', 'Bias': 'Center', 'Agree': 9, 'Disagree': 9} , 
    {'Source': 'News Dakota', 'Bias': 'Center', 'Agree': 10, 'Disagree': 14} , 
    {'Source': 'News Letter Journal', 'Bias': 'Center', 'Agree': 7, 'Disagree': 8} , 
    {'Source': 'News Literacy Project', 'Bias': 'Center', 'Agree': 84, 'Disagree': 83} , 
    {'Source': 'News One', 'Bias': 'Lean Left', 'Agree': 15, 'Disagree': 25} , 
    {'Source': 'News Radio 1200 WOAI', 'Bias': 'Center', 'Agree': 15, 'Disagree': 15} , 
    {'Source': 'NewsBreak', 'Bias': 'Lean Left', 'Agree': 12, 'Disagree': 15} , 
    {'Source': 'NewsBusters', 'Bias': 'Right', 'Agree': 751, 'Disagree': 430} , 
    {'Source': 'Newsday', 'Bias': 'Center', 'Agree': 35, 'Disagree': 41} , 
    {'Source': 'Newsmax (News)', 'Bias': 'Right', 'Agree': 13763, 'Disagree': 12529} , 
    {'Source': 'Newsmax - Opinion', 'Bias': 'Right', 'Agree': 775, 'Disagree': 255} , 
    {'Source': 'NewsNation', 'Bias': 'Center', 'Agree': 1726, 'Disagree': 1708} , 
    {'Source': 'NewsOne', 'Bias': 'Left', 'Agree': 309, 'Disagree': 144} , 
    {'Source': 'Newstimes', 'Bias': 'Center', 'Agree': 11, 'Disagree': 15} , 
    {'Source': 'Newsweek', 'Bias': 'Center', 'Agree': 6325, 'Disagree': 11541} , 
    {'Source': 'Newt Gingrich', 'Bias': 'Right', 'Agree': 945, 'Disagree': 409} , 
    {'Source': 'Newtrals', 'Bias': 'Center', 'Agree': 54, 'Disagree': 45} , 
    {'Source': 'NHPR', 'Bias': 'Center', 'Agree': 6, 'Disagree': 50} , 
    {'Source': 'Nicholas Chronicle', 'Bias': 'Center', 'Agree': 6, 'Disagree': 8} , 
    {'Source': 'Nicholas Kristof', 'Bias': 'Left', 'Agree': 470, 'Disagree': 421} , 
    {'Source': 'Nick Anderson (cartoonist)', 'Bias': 'Center', 'Agree': 75, 'Disagree': 97} , 
    {'Source': 'Nieman Lab', 'Bias': 'Center', 'Agree': 165, 'Disagree': 170} , 
    {'Source': 'NJ Spotlight News', 'Bias': 'Lean Left', 'Agree': 7, 'Disagree': 12} , 
    {'Source': 'nj.com', 'Bias': 'Lean Left', 'Agree': 56, 'Disagree': 63} , 
    {'Source': 'NJ.com News', 'Bias': 'Center', 'Agree': 17, 'Disagree': 22} , 
    {'Source': 'NMPolitics.net', 'Bias': 'Center', 'Agree': 267, 'Disagree': 326} , 
    {'Source': 'No Labels', 'Bias': 'Center', 'Agree': 196, 'Disagree': 164} , 
    {'Source': 'Noah Rothman', 'Bias': 'Lean Right', 'Agree': 111, 'Disagree': 113} , 
    {'Source': 'Noah Smith', 'Bias': 'Lean Left', 'Agree': 52, 'Disagree': 62} , 
    {'Source': 'Norfolk Daily News', 'Bias': 'Center', 'Agree': 13, 'Disagree': 14} , 
    {'Source': 'North Carolina Health News', 'Bias': 'Lean Left', 'Agree': 8, 'Disagree': 9} , 
    {'Source': 'North Country Public Radio', 'Bias': 'Lean Left', 'Agree': 11, 'Disagree': 54} , 
    {'Source': 'North Escambia News', 'Bias': 'Center', 'Agree': 10, 'Disagree': 11} , 
    {'Source': 'North Jersey News', 'Bias': 'Center', 'Agree': 12, 'Disagree': 24} , 
    {'Source': 'North Wright County Today', 'Bias': 'Center', 'Agree': 13, 'Disagree': 13} , 
    {'Source': 'Northern Virginia Magazine', 'Bias': 'Center', 'Agree': 8, 'Disagree': 23} , 
    {'Source': 'Northwest Arkansas Democrat Gazette', 'Bias': 'Center', 'Agree': 27, 'Disagree': 25} , 
    {'Source': 'NowThis News', 'Bias': 'Lean Left', 'Agree': 89, 'Disagree': 96} , 
    {'Source': 'NPR (Online News)', 'Bias': 'Lean Left', 'Agree': 35331, 'Disagree': 35969} , 
    {'Source': 'NPR (Opinion)', 'Bias': 'Lean Left', 'Agree': 10541, 'Disagree': 12958} , 
    {'Source': 'NPR Illinois', 'Bias': 'Lean Left', 'Agree': 15, 'Disagree': 86} , 
    {'Source': 'NPR Michigan Radio', 'Bias': 'Center', 'Agree': 20, 'Disagree': 86} , 
    {'Source': 'NPR Utah KUER', 'Bias': 'Center', 'Agree': 19, 'Disagree': 82} , 
    {'Source': 'NTD', 'Bias': 'Lean Right', 'Agree': 50, 'Disagree': 51} , 
    {'Source': 'Nutfield News', 'Bias': 'Center', 'Agree': 8, 'Disagree': 10} , 
    {'Source': 'NYNMedia', 'Bias': 'Left', 'Agree': 70, 'Disagree': 29} , 
    {'Source': 'Occupy Democrats', 'Bias': 'Left', 'Agree': 89, 'Disagree': 36} , 
    {'Source': 'Odessa American', 'Bias': 'Center', 'Agree': 10, 'Disagree': 10} , 
    {'Source': 'Ohio Capital Journal', 'Bias': 'Lean Left', 'Agree': 70, 'Disagree': 52} , 
    {'Source': 'Oil City News', 'Bias': 'Center', 'Agree': 13, 'Disagree': 17} , 
    {'Source': 'OilPrice.com', 'Bias': 'Center', 'Agree': 50, 'Disagree': 44} , 
    {'Source': 'OKC Friday', 'Bias': 'Center', 'Agree': 9, 'Disagree': 8} , 
    {'Source': 'Oklahoma Watch', 'Bias': 'Center', 'Agree': 8, 'Disagree': 9} , 
    {'Source': 'Omaha World-Herald', 'Bias': 'Center', 'Agree': 25, 'Disagree': 34} , 
    {'Source': 'One America News Network (OAN)', 'Bias': 'Right', 'Agree': 4067, 'Disagree': 2106} , 
    {'Source': 'One Nation News', 'Bias': 'Lean Left', 'Agree': 12, 'Disagree': 13} , 
    {'Source': 'OpenSecrets.org', 'Bias': 'Center', 'Agree': 825, 'Disagree': 603} , 
    {'Source': 'Orange County Register', 'Bias': 'Lean Right', 'Agree': 489, 'Disagree': 408} , 
    {'Source': 'Oregon Public Broadcasting', 'Bias': 'Center', 'Agree': 22, 'Disagree': 68} , 
    {'Source': 'Orlando Sentinel', 'Bias': 'Center', 'Agree': 56, 'Disagree': 122} , 
    {'Source': 'Ottumwa Courier', 'Bias': 'Center', 'Agree': 41, 'Disagree': 41} , 
    {'Source': 'Ottumwa Post', 'Bias': 'Center', 'Agree': 14, 'Disagree': 11} , 
    {'Source': 'Ouachita Citizen', 'Bias': 'Center', 'Agree': 11, 'Disagree': 12} , 
    {'Source': 'Our.News', 'Bias': 'Center', 'Agree': 49, 'Disagree': 52} , 
    {'Source': 'Out', 'Bias': 'Left', 'Agree': 54, 'Disagree': 19} , 
    {'Source': 'Out In Jersey', 'Bias': 'Lean Left', 'Agree': 12, 'Disagree': 20} , 
    {'Source': 'OutKick', 'Bias': 'Lean Right', 'Agree': 108, 'Disagree': 209} , 
    {'Source': 'Pacific Research Institute', 'Bias': 'Right', 'Agree': 270, 'Disagree': 308} , 
    {'Source': 'Pacific Standard', 'Bias': 'Lean Left', 'Agree': 496, 'Disagree': 455} , 
    {'Source': 'Pahrump Valley Times', 'Bias': 'Center', 'Agree': 11, 'Disagree': 9} , 
    {'Source': 'Paintsville Herald', 'Bias': 'Center', 'Agree': 11, 'Disagree': 13} , 
    {'Source': 'Palestine Herald-Press', 'Bias': 'Center', 'Agree': 7, 'Disagree': 10} , 
    {'Source': 'Palladium Magazine', 'Bias': 'Center', 'Agree': 15, 'Disagree': 23} , 
    {'Source': 'Palm Beach News Central', 'Bias': 'Center', 'Agree': 12, 'Disagree': 14} , 
    {'Source': 'Palm Springs Desert Sun', 'Bias': 'Center', 'Agree': 45, 'Disagree': 49} , 
    {'Source': 'Panola Watchman', 'Bias': 'Center', 'Agree': 6, 'Disagree': 7} , 
    {'Source': 'Park Record', 'Bias': 'Center', 'Agree': 16, 'Disagree': 15} , 
    {'Source': 'Pasadena Now', 'Bias': 'Center', 'Agree': 9, 'Disagree': 9} , 
    {'Source': 'Pasadena Star-News', 'Bias': 'Center', 'Agree': 62, 'Disagree': 66} , 
    {'Source': 'Pat Buchanan', 'Bias': 'Right', 'Agree': 286, 'Disagree': 139} , 
    {'Source': 'Pat Oliphant (cartoonist)', 'Bias': 'Center', 'Agree': 92, 'Disagree': 102} , 
    {'Source': 'Patch.com', 'Bias': 'Center', 'Agree': 95, 'Disagree': 165} , 
    {'Source': 'Paul Brandus', 'Bias': 'Center', 'Agree': 35, 'Disagree': 47} , 
    {'Source': 'Paul Krugman', 'Bias': 'Left', 'Agree': 856, 'Disagree': 491} , 
    {'Source': 'Paul Mulholland', 'Bias': 'Lean Left', 'Agree': 33, 'Disagree': 45} , 
    {'Source': 'Paul Szep (cartoonist)', 'Bias': 'Center', 'Agree': 90, 'Disagree': 86} , 
    {'Source': 'Paul Volcker', 'Bias': 'Center', 'Agree': 110, 'Disagree': 93} , 
    {'Source': 'Paul Waldman', 'Bias': 'Left', 'Agree': 82, 'Disagree': 44} , 
    {'Source': 'PBS NewsHour', 'Bias': 'Lean Left', 'Agree': 4380, 'Disagree': 3495} , 
    {'Source': 'Pea Ridge Times', 'Bias': 'Center', 'Agree': 10, 'Disagree': 11} , 
    {'Source': 'Peacock Panache', 'Bias': 'Left', 'Agree': 247, 'Disagree': 144} , 
    {'Source': 'Peak of Ohio', 'Bias': 'Center', 'Agree': 7, 'Disagree': 9} , 
    {'Source': 'Pedro Silva', 'Bias': 'Center', 'Agree': 55, 'Disagree': 82} , 
    {'Source': 'Peggy Noonan', 'Bias': 'Right', 'Agree': 463, 'Disagree': 741} , 
    {'Source': 'Peninsula Clarion', 'Bias': 'Center', 'Agree': 25, 'Disagree': 24} , 
    {'Source': 'Pennsylvania Capital-Star', 'Bias': 'Lean Right', 'Agree': 46, 'Disagree': 53} , 
    {'Source': 'Pensacola News Journal', 'Bias': 'Center', 'Agree': 18, 'Disagree': 22} , 
    {'Source': 'People', 'Bias': 'Lean Left', 'Agree': 73, 'Disagree': 78} , 
    {'Source': 'People for the American Way', 'Bias': 'Left', 'Agree': 473, 'Disagree': 273} , 
    {'Source': 'Peoria Journal Star', 'Bias': 'Center', 'Agree': 12, 'Disagree': 10} , 
    {'Source': 'Persuasion', 'Bias': 'Center', 'Agree': 20, 'Disagree': 20} , 
    {'Source': 'Pete Weichlein', 'Bias': 'Center', 'Agree': 17, 'Disagree': 22} , 
    {'Source': 'Peter Boghossian', 'Bias': 'Center', 'Agree': 18, 'Disagree': 13} , 
    {'Source': 'Peter Roff', 'Bias': 'Lean Right', 'Agree': 405, 'Disagree': 215} , 
    {'Source': 'Peter Thiel', 'Bias': 'Lean Right', 'Agree': 140, 'Disagree': 208} , 
    {'Source': 'Pew Research Center', 'Bias': 'Center', 'Agree': 3163, 'Disagree': 1929} , 
    {'Source': 'Philadelphia Gay News', 'Bias': 'Lean Left', 'Agree': 22, 'Disagree': 30} , 
    {'Source': 'Phillip Bader', 'Bias': 'Center', 'Agree': 64, 'Disagree': 77} , 
    {'Source': 'Phoenix New Times', 'Bias': 'Center', 'Agree': 11, 'Disagree': 16} , 
    {'Source': 'Phoenix New Times', 'Bias': 'Center', 'Agree': 6, 'Disagree': 11} , 
    {'Source': 'Phys.org', 'Bias': 'Center', 'Agree': 346, 'Disagree': 213} , 
    {'Source': 'Physicians for a National Health Program', 'Bias': 'Left', 'Agree': 305, 'Disagree': 194} , 
    {'Source': 'Physicians for Life', 'Bias': 'Lean Right', 'Agree': 33, 'Disagree': 58} , 
    {'Source': 'Piers Morgan', 'Bias': 'Lean Left', 'Agree': 612, 'Disagree': 1168} , 
    {'Source': 'PinkNews', 'Bias': 'Left', 'Agree': 294, 'Disagree': 108} , 
    {'Source': 'Pioneer Press', 'Bias': 'Center', 'Agree': 20, 'Disagree': 25} , 
    {'Source': 'Pittsburgh Post-Gazette', 'Bias': 'Center', 'Agree': 432, 'Disagree': 537} , 
    {'Source': 'Pittsburgh Tribune-Review', 'Bias': 'Center', 'Agree': 18, 'Disagree': 38} , 
    {'Source': 'PJ Media', 'Bias': 'Right', 'Agree': 838, 'Disagree': 367} , 
    {'Source': 'Plainsman', 'Bias': 'Center', 'Agree': 9, 'Disagree': 10} , 
    {'Source': 'Plaquemines Gazette', 'Bias': 'Center', 'Agree': 9, 'Disagree': 11} , 
    {'Source': 'Political Empathy Project', 'Bias': 'Center', 'Agree': 18, 'Disagree': 19} , 
    {'Source': 'Politico', 'Bias': 'Lean Left', 'Agree': 26299, 'Disagree': 33898} , 
    {'Source': 'Politics PA', 'Bias': 'Lean Left', 'Agree': 7, 'Disagree': 14} , 
    {'Source': 'PoliticusUSA', 'Bias': 'Left', 'Agree': 1260, 'Disagree': 457} , 
    {'Source': 'Pope County Tribune', 'Bias': 'Center', 'Agree': 17, 'Disagree': 18} , 
    {'Source': 'Port Aransas South Jetty News', 'Bias': 'Center', 'Agree': 9, 'Disagree': 10} , 
    {'Source': 'Portland Press Herald', 'Bias': 'Center', 'Agree': 344, 'Disagree': 524} , 
    {'Source': 'Post Independent', 'Bias': 'Center', 'Agree': 10, 'Disagree': 11} , 
    {'Source': 'Post Register', 'Bias': 'Center', 'Agree': 17, 'Disagree': 20} , 
    {'Source': 'Post-Bulletin', 'Bias': 'Center', 'Agree': 23, 'Disagree': 19} , 
    {'Source': 'Poughkeepsie Journal', 'Bias': 'Center', 'Agree': 12, 'Disagree': 14} , 
    {'Source': 'Poynter', 'Bias': 'Center', 'Agree': 250, 'Disagree': 546} , 
    {'Source': 'Prager University', 'Bias': 'Right', 'Agree': 4343, 'Disagree': 1033} , 
    {'Source': 'Premier Christian News', 'Bias': 'Lean Left', 'Agree': 21, 'Disagree': 19} , 
    {'Source': 'PRI (Public Radio International)', 'Bias': 'Center', 'Agree': 855, 'Disagree': 627} , 
    {'Source': 'Progressive Voices of Iowa', 'Bias': 'Left', 'Agree': 323, 'Disagree': 189} , 
    {'Source': 'Project Veritas', 'Bias': 'Right', 'Agree': 664, 'Disagree': 704} , 
    {'Source': 'ProPublica', 'Bias': 'Lean Left', 'Agree': 2343, 'Disagree': 1653} , 
    {'Source': 'Psych Central', 'Bias': 'Center', 'Agree': 22, 'Disagree': 43} , 
    {'Source': 'Psychology Today', 'Bias': 'Center', 'Agree': 221, 'Disagree': 279} , 
    {'Source': 'Public News Service', 'Bias': 'Center', 'Agree': 16, 'Disagree': 27} , 
    {'Source': 'Quartz', 'Bias': 'Center', 'Agree': 872, 'Disagree': 1024} , 
    {'Source': 'Queerty', 'Bias': 'Left', 'Agree': 50, 'Disagree': 15} , 
    {'Source': 'Quillette', 'Bias': 'Lean Right', 'Agree': 707, 'Disagree': 1040} , 
    {'Source': 'Quin Hillyer', 'Bias': 'Lean Right', 'Agree': 39, 'Disagree': 50} , 
    {'Source': 'Quinnipiac University', 'Bias': 'Center', 'Agree': 326, 'Disagree': 563} , 
    {'Source': 'Rachel Eckhardt', 'Bias': 'Lean Left', 'Agree': 104, 'Disagree': 127} , 
    {'Source': 'Racket News', 'Bias': 'Center', 'Agree': 7, 'Disagree': 4} , 
    {'Source': 'Radio Iowa', 'Bias': 'Center', 'Agree': 13, 'Disagree': 20} , 
    {'Source': 'Rahm Emanuel', 'Bias': 'Lean Left', 'Agree': 116, 'Disagree': 338} , 
    {'Source': 'Ralph Benko', 'Bias': 'Right', 'Agree': 143, 'Disagree': 211} , 
    {'Source': 'Ramesh Ponnuru', 'Bias': 'Right', 'Agree': 223, 'Disagree': 238} , 
    {'Source': 'RAND Corporation', 'Bias': 'Lean Left', 'Agree': 678, 'Disagree': 917} , 
    {'Source': 'Rand Paul', 'Bias': 'Lean Right', 'Agree': 654, 'Disagree': 569} , 
    {'Source': 'Rapid City Journal', 'Bias': 'Center', 'Agree': 22, 'Disagree': 22} , 
    {'Source': 'Rasmussen Reports', 'Bias': 'Lean Right', 'Agree': 790, 'Disagree': 1097} , 
    {'Source': 'Raw Story', 'Bias': 'Left', 'Agree': 2006, 'Disagree': 778} , 
    {'Source': 'Reading Eagle', 'Bias': 'Center', 'Agree': 16, 'Disagree': 14} , 
    {'Source': 'RealClearPolitics', 'Bias': 'Center', 'Agree': 4776, 'Disagree': 5843} , 
    {'Source': 'Reason', 'Bias': 'Lean Right', 'Agree': 10739, 'Disagree': 6958} , 
    {'Source': 'Reason Foundation', 'Bias': 'Lean Right', 'Agree': 404, 'Disagree': 449} , 
    {'Source': 'Rebecca Sheehan', 'Bias': 'Lean Right', 'Agree': 49, 'Disagree': 64} , 
    {'Source': 'Record Journal', 'Bias': 'Center', 'Agree': 212, 'Disagree': 220} , 
    {'Source': 'Record-Courier', 'Bias': 'Center', 'Agree': 12, 'Disagree': 15} , 
    {'Source': 'Red Lake Nation News', 'Bias': 'Center', 'Agree': 20, 'Disagree': 18} , 
    {'Source': 'Red Racing Horses', 'Bias': 'Right', 'Agree': 80, 'Disagree': 101} , 
    {'Source': 'RedBlueDictionary.org', 'Bias': 'Mixed', 'Agree': 223, 'Disagree': 177} , 
    {'Source': 'redefinED', 'Bias': 'Center', 'Agree': 192, 'Disagree': 114} , 
    {'Source': 'Redlands Daily Facts', 'Bias': 'Center', 'Agree': 45, 'Disagree': 51} , 
    {'Source': 'RedState', 'Bias': 'Right', 'Agree': 1013, 'Disagree': 396} , 
    {'Source': 'Refinery29', 'Bias': 'Left', 'Agree': 162, 'Disagree': 108} , 
    {'Source': 'Register Citizen', 'Bias': 'Lean Left', 'Agree': 22, 'Disagree': 23} , 
    {'Source': 'Relevant Magazine', 'Bias': 'Lean Left', 'Agree': 12, 'Disagree': 17} , 
    {'Source': 'Religion News Service', 'Bias': 'Center', 'Agree': 36, 'Disagree': 47} , 
    {'Source': 'Rem Reider', 'Bias': 'Center', 'Agree': 135, 'Disagree': 143} , 
    {'Source': 'Reno News & Review', 'Bias': 'Center', 'Agree': 13, 'Disagree': 12} , 
    {'Source': 'Republican Party', 'Bias': 'Lean Right', 'Agree': 266, 'Disagree': 358} , 
    {'Source': 'Reuters', 'Bias': 'Center', 'Agree': 24100, 'Disagree': 14753} , 
    {'Source': 'Rev. Barbara Ann Michaels, Jester of the Peace', 'Bias': 'Lean Left', 'Agree': 20, 'Disagree': 31} , 
    {'Source': 'Rev. Jesse Jackson Sr.', 'Bias': 'Left', 'Agree': 723, 'Disagree': 245} , 
    {'Source': 'Revolver News', 'Bias': 'Right', 'Agree': 109, 'Disagree': 106} , 
    {'Source': 'Rex Huppke', 'Bias': 'Left', 'Agree': 171, 'Disagree': 37} , 
    {'Source': 'Rich Lowry', 'Bias': 'Right', 'Agree': 390, 'Disagree': 406} , 
    {'Source': 'Rich Tafel', 'Bias': 'Center', 'Agree': 124, 'Disagree': 110} , 
    {'Source': 'Rich Zeoli', 'Bias': 'Lean Right', 'Agree': 148, 'Disagree': 124} , 
    {'Source': 'Richard K. Sherwin', 'Bias': 'Lean Left', 'Agree': 23, 'Disagree': 22} , 
    {'Source': 'Richard M. Cohen', 'Bias': 'Lean Left', 'Agree': 82, 'Disagree': 83} , 
    {'Source': 'Richard Perrins', 'Bias': 'Center', 'Agree': 25, 'Disagree': 35} , 
    {'Source': 'Richardson Today', 'Bias': 'Center', 'Agree': 7, 'Disagree': 7} , 
    {'Source': 'Richland Source', 'Bias': 'Center', 'Agree': 10, 'Disagree': 12} , 
    {'Source': 'Richmond Times Dispatch', 'Bias': 'Lean Right', 'Agree': 357, 'Disagree': 352} , 
    {'Source': 'Rick Snyder', 'Bias': 'Lean Right', 'Agree': 38, 'Disagree': 44} , 
    {'Source': 'Rick Ungar', 'Bias': 'Lean Left', 'Agree': 210, 'Disagree': 192} , 
    {'Source': 'Rick Wytmar', 'Bias': 'Lean Left', 'Agree': 55, 'Disagree': 70} , 
    {'Source': 'Right Guest Commentaries', 'Bias': 'Right', 'Agree': 117, 'Disagree': 91} , 
    {'Source': 'Right Side News', 'Bias': 'Right', 'Agree': 569, 'Disagree': 300} , 
    {'Source': 'Right Wing News', 'Bias': 'Right', 'Agree': 493, 'Disagree': 257} , 
    {'Source': 'Ripon Commonwealth Press', 'Bias': 'Center', 'Agree': 10, 'Disagree': 7} , 
    {'Source': 'Risen Magazine', 'Bias': 'Center', 'Agree': 35, 'Disagree': 13} , 
    {'Source': 'Rob Anderson', 'Bias': 'Lean Left', 'Agree': 9, 'Disagree': 12} , 
    {'Source': 'Rob Rogers (cartoonist)', 'Bias': 'Left', 'Agree': 116, 'Disagree': 48} , 
    {'Source': 'Robbie Robinette', 'Bias': 'Center', 'Agree': 20, 'Disagree': 27} , 
    {'Source': 'Robby Soave', 'Bias': 'Lean Right', 'Agree': 72, 'Disagree': 63} , 
    {'Source': 'Robert Ariail (cartoonist)', 'Bias': 'Center', 'Agree': 97, 'Disagree': 113} , 
    {'Source': 'Robert Reich', 'Bias': 'Left', 'Agree': 140, 'Disagree': 74} , 
    {'Source': 'Robert Samuelson', 'Bias': 'Center', 'Agree': 174, 'Disagree': 198} , 
    {'Source': 'Robert Verbruggen', 'Bias': 'Lean Right', 'Agree': 44, 'Disagree': 52} , 
    {'Source': 'Robert Weissman', 'Bias': 'Lean Left', 'Agree': 20, 'Disagree': 21} , 
    {'Source': 'Rockwall Herald Banner', 'Bias': 'Center', 'Agree': 5, 'Disagree': 5} , 
    {'Source': 'Rod Blagojevich', 'Bias': 'Center', 'Agree': 65, 'Disagree': 183} , 
    {'Source': 'Rod Eccles', 'Bias': 'Right', 'Agree': 13, 'Disagree': 41} , 
    {'Source': 'Rogue River Press', 'Bias': 'Center', 'Agree': 11, 'Disagree': 11} , 
    {'Source': 'Rolf Hendriks', 'Bias': 'Center', 'Agree': 71, 'Disagree': 75} , 
    {'Source': 'Roll Call', 'Bias': 'Center', 'Agree': 395, 'Disagree': 392} , 
    {'Source': 'RollingStone.com', 'Bias': 'Left', 'Agree': 2731, 'Disagree': 682} , 
    {'Source': 'Ron Suskind', 'Bias': 'Center', 'Agree': 32, 'Disagree': 29} , 
    {'Source': 'Rose Mercer', 'Bias': 'Lean Left', 'Agree': 29, 'Disagree': 38} , 
    {'Source': 'Ross Douthat', 'Bias': 'Lean Right', 'Agree': 305, 'Disagree': 230} , 
    {'Source': 'RT', 'Bias': 'Lean Right', 'Agree': 245, 'Disagree': 329} , 
    {'Source': 'Russell Brandom', 'Bias': 'Center', 'Agree': 47, 'Disagree': 57} , 
    {'Source': 'Ruston Daily Leader', 'Bias': 'Center', 'Agree': 20, 'Disagree': 20} , 
    {'Source': 'Ruth Marcus', 'Bias': 'Lean Left', 'Agree': 328, 'Disagree': 349} , 
    {'Source': 'Rutland Herald', 'Bias': 'Center', 'Agree': 18, 'Disagree': 17} , 
    {'Source': 'Ryan Bomberger', 'Bias': 'Right', 'Agree': 47, 'Disagree': 72} , 
    {'Source': 'Ryan Cooper', 'Bias': 'Left', 'Agree': 176, 'Disagree': 122} , 
    {'Source': 'Ryan Cooper', 'Bias': 'Left', 'Agree': 615, 'Disagree': 167} , 
    {'Source': 'S.E. Cupp', 'Bias': 'Lean Right', 'Agree': 154, 'Disagree': 226} , 
    {'Source': 'Saagar Enjeti', 'Bias': 'Center', 'Agree': 230, 'Disagree': 241} , 
    {'Source': 'Salem News', 'Bias': 'Center', 'Agree': 13, 'Disagree': 16} , 
    {'Source': 'Salina Journal', 'Bias': 'Center', 'Agree': 13, 'Disagree': 10} , 
    {'Source': 'Sally Pipes', 'Bias': 'Right', 'Agree': 342, 'Disagree': 203} , 
    {'Source': 'Salon', 'Bias': 'Left', 'Agree': 12337, 'Disagree': 5449} , 
    {'Source': 'Sam Harris', 'Bias': 'Center', 'Agree': 143, 'Disagree': 117} , 
    {'Source': 'Sam Seder', 'Bias': 'Left', 'Agree': 147, 'Disagree': 33} , 
    {'Source': 'Samantha Shireman', 'Bias': 'Lean Left', 'Agree': 78, 'Disagree': 83} , 
    {'Source': 'Samuel Shroff', 'Bias': 'Left', 'Agree': 19, 'Disagree': 8} , 
    {'Source': 'San Antonio Express-News', 'Bias': 'Center', 'Agree': 87, 'Disagree': 138} , 
    {'Source': 'San Bernardino Sun', 'Bias': 'Center', 'Agree': 55, 'Disagree': 54} , 
    {'Source': 'San Diego Union-Tribune', 'Bias': 'Lean Left', 'Agree': 130, 'Disagree': 128} , 
    {'Source': 'San Francisco Chronicle', 'Bias': 'Left', 'Agree': 1313, 'Disagree': 563} , 
    {'Source': 'San Gabriel Valley Tribune', 'Bias': 'Center', 'Agree': 56, 'Disagree': 57} , 
    {'Source': 'San Jose Mercury News', 'Bias': 'Lean Left', 'Agree': 596, 'Disagree': 616} , 
    {'Source': 'Santa Fe New Mexican', 'Bias': 'Center', 'Agree': 27, 'Disagree': 29} , 
    {'Source': 'Sara Luterman', 'Bias': 'Lean Left', 'Agree': 21, 'Disagree': 28} , 
    {'Source': 'Sarah Palin', 'Bias': 'Right', 'Agree': 40, 'Disagree': 27} , 
    {'Source': 'SBG', 'Bias': 'Center', 'Agree': 109, 'Disagree': 123} , 
    {'Source': 'Science Daily', 'Bias': 'Center', 'Agree': 682, 'Disagree': 423} , 
    {'Source': 'Scientific American', 'Bias': 'Lean Left', 'Agree': 2230, 'Disagree': 1225} , 
    {'Source': 'Scott Adams', 'Bias': 'Center', 'Agree': 149, 'Disagree': 164} , 
    {'Source': 'Scott Jennings', 'Bias': 'Lean Right', 'Agree': 105, 'Disagree': 93} , 
    {'Source': 'Scott Stantis (cartoonist)', 'Bias': 'Right', 'Agree': 84, 'Disagree': 132} , 
    {'Source': 'Scottsbluff Star-Herald', 'Bias': 'Center', 'Agree': 16, 'Disagree': 18} , 
    {'Source': 'SCOTUSblog', 'Bias': 'Center', 'Agree': 133, 'Disagree': 137} , 
    {'Source': 'Scriberr Media - News', 'Bias': 'Center', 'Agree': 121, 'Disagree': 111} , 
    {'Source': 'Scriberr Media - Opinion/Editorial', 'Bias': 'Lean Right', 'Agree': 53, 'Disagree': 58} , 
    {'Source': 'Scripps News', 'Bias': 'Center', 'Agree': 705, 'Disagree': 564} , 
    {'Source': 'Seacoast Online', 'Bias': 'Center', 'Agree': 8, 'Disagree': 7} , 
    {'Source': 'Sean McDowell', 'Bias': 'Right', 'Agree': 11, 'Disagree': 32} , 
    {'Source': 'Search for Common Ground', 'Bias': 'Center', 'Agree': 12, 'Disagree': 9} , 
    {'Source': 'Searchlight New Mexico', 'Bias': 'Center', 'Agree': 4, 'Disagree': 5} , 
    {'Source': 'Seattle Gay News', 'Bias': 'Lean Left', 'Agree': 13, 'Disagree': 24} , 
    {'Source': 'Seeds of Peace', 'Bias': 'Center', 'Agree': 12, 'Disagree': 13} , 
    {'Source': 'Seeley Swan Pathfinder', 'Bias': 'Center', 'Agree': 7, 'Disagree': 8} , 
    {'Source': 'Seguin Today', 'Bias': 'Center', 'Agree': 6, 'Disagree': 5} , 
    {'Source': 'Semafor', 'Bias': 'Lean Left', 'Agree': 84, 'Disagree': 140} , 
    {'Source': 'Sen. Jim Risch', 'Bias': 'Lean Right', 'Agree': 22, 'Disagree': 27} , 
    {'Source': 'Sentinel-Tribune', 'Bias': 'Center', 'Agree': 6, 'Disagree': 9} , 
    {'Source': 'Seth Tower Hurd', 'Bias': 'Lean Right', 'Agree': 52, 'Disagree': 48} , 
    {'Source': 'Seven Days News', 'Bias': 'Center', 'Agree': 10, 'Disagree': 10} , 
    {'Source': 'SF Weekly', 'Bias': 'Center', 'Agree': 342, 'Disagree': 440} , 
    {'Source': 'SFGATE', 'Bias': 'Lean Left', 'Agree': 676, 'Disagree': 726} , 
    {'Source': 'Shanice Jones', 'Bias': 'Center', 'Agree': 17, 'Disagree': 21} , 
    {'Source': 'Shannon Mannon', 'Bias': 'Lean Left', 'Agree': 53, 'Disagree': 57} , 
    {'Source': 'Shore News Network', 'Bias': 'Center', 'Agree': 17, 'Disagree': 17} , 
    {'Source': 'Shreveport Times', 'Bias': 'Center', 'Agree': 36, 'Disagree': 44} , 
    {'Source': 'Signe Wilkinson (cartoonist)', 'Bias': 'Left', 'Agree': 84, 'Disagree': 54} , 
    {'Source': 'Silver City Daily Press', 'Bias': 'Center', 'Agree': 11, 'Disagree': 12} , 
    {'Source': 'Siouxland Proud', 'Bias': 'Center', 'Agree': 18, 'Disagree': 16} , 
    {'Source': 'Sky-Hi Daily News', 'Bias': 'Lean Left', 'Agree': 222, 'Disagree': 230} , 
    {'Source': 'Slate', 'Bias': 'Left', 'Agree': 11573, 'Disagree': 4166} , 
    {'Source': 'Slavoj Žižek', 'Bias': 'Left', 'Agree': 17, 'Disagree': 7} , 
    {'Source': 'Small World (cartoonist)', 'Bias': 'Left', 'Agree': 92, 'Disagree': 63} , 
    {'Source': 'SmartHER News', 'Bias': 'Center', 'Agree': 18, 'Disagree': 16} , 
    {'Source': 'SmartNews', 'Bias': 'Lean Left', 'Agree': 3, 'Disagree': 0} , 
    {'Source': 'Smerconish', 'Bias': 'Center', 'Agree': 336, 'Disagree': 412} , 
    {'Source': 'Smithsonian Magazine', 'Bias': 'Center', 'Agree': 220, 'Disagree': 192} , 
    {'Source': 'Soap Box Media Cincinnati', 'Bias': 'Center', 'Agree': 7, 'Disagree': 11} , 
    {'Source': 'Socialist Alternative', 'Bias': 'Left', 'Agree': 605, 'Disagree': 276} , 
    {'Source': 'Socialist Project/The Bullet', 'Bias': 'Left', 'Agree': 515, 'Disagree': 243} , 
    {'Source': 'South Arkansas Sun', 'Bias': 'Center', 'Agree': 6, 'Disagree': 10} , 
    {'Source': 'South Bend Tribune', 'Bias': 'Center', 'Agree': 20, 'Disagree': 23} , 
    {'Source': 'South Carolina Public Radio', 'Bias': 'Center', 'Agree': 9, 'Disagree': 41} , 
    {'Source': 'South China Morning Post', 'Bias': 'Center', 'Agree': 247, 'Disagree': 247} , 
    {'Source': 'South Dakota News Watch', 'Bias': 'Center', 'Agree': 9, 'Disagree': 6} , 
    {'Source': 'South Florida Gay News', 'Bias': 'Lean Left', 'Agree': 9, 'Disagree': 18} , 
    {'Source': 'Southeast Missourian', 'Bias': 'Center', 'Agree': 13, 'Disagree': 11} , 
    {'Source': 'Southern Minnesota News', 'Bias': 'Center', 'Agree': 15, 'Disagree': 11} , 
    {'Source': 'Southern Poverty Law Center', 'Bias': 'Left', 'Agree': 310, 'Disagree': 64} , 
    {'Source': 'Southern Utah News', 'Bias': 'Center', 'Agree': 10, 'Disagree': 11} , 
    {'Source': 'Southwest Arkansas Radio', 'Bias': 'Center', 'Agree': 8, 'Disagree': 16} , 
    {'Source': 'Sparks Tribune', 'Bias': 'Center', 'Agree': 8, 'Disagree': 10} , 
    {'Source': 'Spectrum Bay News 9', 'Bias': 'Center', 'Agree': 7, 'Disagree': 9} , 
    {'Source': 'Spectrum News NY1', 'Bias': 'Center', 'Agree': 15, 'Disagree': 19} , 
    {'Source': 'Spiked', 'Bias': 'Lean Right', 'Agree': 154, 'Disagree': 160} , 
    {'Source': 'Splinter', 'Bias': 'Left', 'Agree': 315, 'Disagree': 177} , 
    {'Source': 'Spokesman Review', 'Bias': 'Lean Left', 'Agree': 323, 'Disagree': 375} , 
    {'Source': 'Spot On Alabama', 'Bias': 'Center', 'Agree': 12, 'Disagree': 11} , 
    {'Source': 'Spot On Florida', 'Bias': 'Center', 'Agree': 10, 'Disagree': 12} , 
    {'Source': 'Spot On Illinois', 'Bias': 'Center', 'Agree': 5, 'Disagree': 7} , 
    {'Source': 'Spotlight PA', 'Bias': 'Center', 'Agree': 11, 'Disagree': 10} , 
    {'Source': 'Spread Great Ideas', 'Bias': 'Center', 'Agree': 24, 'Disagree': 21} , 
    {'Source': 'Springfield Daily Citizen', 'Bias': 'Center', 'Agree': 8, 'Disagree': 11} , 
    {'Source': 'Springfield News-Leader', 'Bias': 'Center', 'Agree': 31, 'Disagree': 29} , 
    {'Source': 'Springfield News-Sun', 'Bias': 'Center', 'Agree': 9, 'Disagree': 10} , 
    {'Source': 'St George News', 'Bias': 'Center', 'Agree': 8, 'Disagree': 15} , 
    {'Source': 'St. Augustine Record', 'Bias': 'Center', 'Agree': 9, 'Disagree': 11} , 
    {'Source': 'St. Cloud Times', 'Bias': 'Lean Left', 'Agree': 16, 'Disagree': 16} , 
    {'Source': 'St. George News', 'Bias': 'Center', 'Agree': 12, 'Disagree': 12} , 
    {'Source': 'St. Joseph News-Press', 'Bias': 'Center', 'Agree': 14, 'Disagree': 18} , 
    {'Source': 'St. Louis Call Newspapers', 'Bias': 'Center', 'Agree': 8, 'Disagree': 10} , 
    {'Source': 'St. Louis Post-Dispatch', 'Bias': 'Center', 'Agree': 63, 'Disagree': 99} , 
    {'Source': 'St. Louis Riverfront Times', 'Bias': 'Lean Left', 'Agree': 11, 'Disagree': 16} , 
    {'Source': 'Stacey Abrams', 'Bias': 'Lean Left', 'Agree': 143, 'Disagree': 382} , 
    {'Source': 'Stamford Advocate', 'Bias': 'Center', 'Agree': 13, 'Disagree': 15} , 
    {'Source': 'Stan Marek', 'Bias': 'Center', 'Agree': 22, 'Disagree': 15} , 
    {'Source': 'StandAmerica', 'Bias': 'Right', 'Agree': 13, 'Disagree': 39} , 
    {'Source': 'Star Beacon', 'Bias': 'Center', 'Agree': 11, 'Disagree': 13} , 
    {'Source': 'Star Democrat', 'Bias': 'Center', 'Agree': 3, 'Disagree': 2} , 
    {'Source': 'Star Tribune', 'Bias': 'Lean Left', 'Agree': 172, 'Disagree': 192} , 
    {'Source': 'Stars and Stripes', 'Bias': 'Center', 'Agree': 74, 'Disagree': 61} , 
    {'Source': 'Starved Rock Media', 'Bias': 'Center', 'Agree': 10, 'Disagree': 11} , 
    {'Source': 'STAT', 'Bias': 'Center', 'Agree': 99, 'Disagree': 102} , 
    {'Source': 'State Journal', 'Bias': 'Lean Left', 'Agree': 251, 'Disagree': 341} , 
    {'Source': 'Staten Island Advance', 'Bias': 'Center', 'Agree': 21, 'Disagree': 15} , 
    {'Source': 'Statesman Journal', 'Bias': 'Center', 'Agree': 24, 'Disagree': 26} , 
    {'Source': 'Stephen Perkins', 'Bias': 'Lean Right', 'Agree': 36, 'Disagree': 38} , 
    {'Source': 'Steve Benen', 'Bias': 'Left', 'Agree': 68, 'Disagree': 38} , 
    {'Source': 'Steve Benson (cartoonist)', 'Bias': 'Left', 'Agree': 123, 'Disagree': 100} , 
    {'Source': 'Steve Breen (cartoonist)', 'Bias': 'Center', 'Agree': 101, 'Disagree': 85} , 
    {'Source': 'Steve Forbes', 'Bias': 'Lean Right', 'Agree': 200, 'Disagree': 122} , 
    {'Source': 'Steve Kelley (cartoonist)', 'Bias': 'Right', 'Agree': 67, 'Disagree': 90} , 
    {'Source': 'Steve Sack (cartoonist)', 'Bias': 'Left', 'Agree': 103, 'Disagree': 55} , 
    {'Source': 'Steven Crowder', 'Bias': 'Right', 'Agree': 119, 'Disagree': 65} , 
    {'Source': 'Steven Petrow', 'Bias': 'Center', 'Agree': 35, 'Disagree': 42} , 
    {'Source': 'Stillwater Gazette', 'Bias': 'Center', 'Agree': 13, 'Disagree': 13} , 
    {'Source': 'Stimson Center', 'Bias': 'Center', 'Agree': 44, 'Disagree': 53} , 
    {'Source': 'Storm Lake Times', 'Bias': 'Center', 'Agree': 14, 'Disagree': 16} , 
    {'Source': 'StoryCorps', 'Bias': 'Mixed', 'Agree': 155, 'Disagree': 140} , 
    {'Source': 'Straight Arrow News', 'Bias': 'Center', 'Agree': 113, 'Disagree': 37} , 
    {'Source': 'Stuart Carlson (cartoonist)', 'Bias': 'Left', 'Agree': 91, 'Disagree': 79} , 
    {'Source': 'Students For Life', 'Bias': 'Lean Right', 'Agree': 70, 'Disagree': 85} , 
    {'Source': 'Subverse', 'Bias': 'Center', 'Agree': 177, 'Disagree': 126} , 
    {'Source': 'Sukhayl Niyazov', 'Bias': 'Center', 'Agree': 68, 'Disagree': 80} , 
    {'Source': 'Sun Herald', 'Bias': 'Center', 'Agree': 13, 'Disagree': 18} , 
    {'Source': 'Sun Sentinel', 'Bias': 'Center', 'Agree': 36, 'Disagree': 38} , 
    {'Source': 'Sunlight Foundation', 'Bias': 'Center', 'Agree': 167, 'Disagree': 194} , 
    {'Source': 'Superior Telegram', 'Bias': 'Center', 'Agree': 8, 'Disagree': 9} , 
    {'Source': 'Suspend Belief Podcast', 'Bias': 'Mixed', 'Agree': 210, 'Disagree': 235} , 
    {'Source': 'SW News 4 U', 'Bias': 'Center', 'Agree': 8, 'Disagree': 10} , 
    {'Source': 'Sweetwater Now', 'Bias': 'Center', 'Agree': 5, 'Disagree': 7} , 
    {'Source': 'Tablet Mag', 'Bias': 'Lean Right', 'Agree': 204, 'Disagree': 170} , 
    {'Source': 'Taipei Times', 'Bias': 'Center', 'Agree': 32, 'Disagree': 34} , 
    {'Source': 'Tallahassee Democrat', 'Bias': 'Center', 'Agree': 379, 'Disagree': 396} , 
    {'Source': 'Tampa Bay Times', 'Bias': 'Center', 'Agree': 104, 'Disagree': 206} , 
    {'Source': 'Tangle', 'Bias': 'Center', 'Agree': 193, 'Disagree': 60} , 
    {'Source': 'Tania Israel', 'Bias': 'Left', 'Agree': 53, 'Disagree': 50} , 
    {'Source': 'Tara D. Sonenshine', 'Bias': 'Center', 'Agree': 27, 'Disagree': 24} , 
    {'Source': 'Tara Parekh', 'Bias': 'Lean Left', 'Agree': 44, 'Disagree': 46} , 
    {'Source': 'Taylor Marshall', 'Bias': 'Right', 'Agree': 13, 'Disagree': 30} , 
    {'Source': 'Tech Xplore', 'Bias': 'Center', 'Agree': 61, 'Disagree': 56} , 
    {'Source': 'TechCrunch', 'Bias': 'Center', 'Agree': 575, 'Disagree': 467} , 
    {'Source': 'Ted Rall (cartoonist)', 'Bias': 'Left', 'Agree': 108, 'Disagree': 76} , 
    {'Source': 'Teen Vogue', 'Bias': 'Left', 'Agree': 577, 'Disagree': 748} , 
    {'Source': 'Telegram & Gazette', 'Bias': 'Center', 'Agree': 15, 'Disagree': 18} , 
    {'Source': 'Tennessee Lookout', 'Bias': 'Lean Left', 'Agree': 13, 'Disagree': 13} , 
    {'Source': 'Texas Insider', 'Bias': 'Center', 'Agree': 7, 'Disagree': 9} , 
    {'Source': 'Texas Monthly', 'Bias': 'Center', 'Agree': 47, 'Disagree': 91} , 
    {'Source': 'Texas Signal', 'Bias': 'Left', 'Agree': 59, 'Disagree': 43} , 
    {'Source': 'Texas Standard', 'Bias': 'Center', 'Agree': 10, 'Disagree': 11} , 
    {'Source': 'Texomas Homepage KFDX 3', 'Bias': 'Center', 'Agree': 11, 'Disagree': 11} , 
    {'Source': 'The Ada News', 'Bias': 'Center', 'Agree': 15, 'Disagree': 18} , 
    {'Source': 'The Advocate', 'Bias': 'Lean Left', 'Agree': 94, 'Disagree': 123} , 
    {'Source': 'The Advocate', 'Bias': 'Center', 'Agree': 18, 'Disagree': 21} , 
    {'Source': 'The Advocate-Messenger', 'Bias': 'Lean Left', 'Agree': 245, 'Disagree': 297} , 
    {'Source': 'The Alaska Landmine', 'Bias': 'Center', 'Agree': 10, 'Disagree': 11} , 
    {'Source': 'The Amarillo Pioneer', 'Bias': 'Center', 'Agree': 4, 'Disagree': 7} , 
    {'Source': 'The American Conservative', 'Bias': 'Right', 'Agree': 525, 'Disagree': 464} , 
    {'Source': 'The American Mind', 'Bias': 'Lean Right', 'Agree': 113, 'Disagree': 117} , 
    {'Source': 'The American Spectator', 'Bias': 'Right', 'Agree': 13093, 'Disagree': 4792} , 
    {'Source': 'The Anniston Star', 'Bias': 'Center', 'Agree': 15, 'Disagree': 18} , 
    {'Source': 'The Appeal', 'Bias': 'Center', 'Agree': 153, 'Disagree': 161} , 
    {'Source': 'The Arab American News', 'Bias': 'Center', 'Agree': 7, 'Disagree': 10} , 
    {'Source': 'The Ardmoreite', 'Bias': 'Center', 'Agree': 8, 'Disagree': 9} , 
    {'Source': 'The Atlanta Voice', 'Bias': 'Lean Left', 'Agree': 16, 'Disagree': 14} , 
    {'Source': 'The Atlantic', 'Bias': 'Left', 'Agree': 17820, 'Disagree': 9966} , 
    {'Source': 'The Augusta Press', 'Bias': 'Center', 'Agree': 5, 'Disagree': 7} , 
    {'Source': 'The Austin Chronicle', 'Bias': 'Left', 'Agree': 0, 'Disagree': 0} , 
    {'Source': 'The Baltimore Banner', 'Bias': 'Center', 'Agree': 11, 'Disagree': 15} , 
    {'Source': 'The Bellows', 'Bias': 'Center', 'Agree': 40, 'Disagree': 38} , 
    {'Source': 'The Bemidji Pioneer', 'Bias': 'Center', 'Agree': 14, 'Disagree': 12} , 
    {'Source': 'The Bend Bulletin', 'Bias': 'Center', 'Agree': 10, 'Disagree': 12} , 
    {'Source': 'The Berkshire Eagle', 'Bias': 'Lean Left', 'Agree': 11, 'Disagree': 15} , 
    {'Source': 'The Berkshire Eagle', 'Bias': 'Center', 'Agree': 14, 'Disagree': 13} , 
    {'Source': 'The Berkshire Edge', 'Bias': 'Center', 'Agree': 10, 'Disagree': 7} , 
    {'Source': 'The Bismarck Tribune', 'Bias': 'Center', 'Agree': 13, 'Disagree': 11} , 
    {'Source': 'The Bismarck Tribune', 'Bias': 'Center', 'Agree': 13, 'Disagree': 17} , 
    {'Source': 'The Black Detour', 'Bias': 'Center', 'Agree': 10, 'Disagree': 12} , 
    {'Source': 'The Blade', 'Bias': 'Center', 'Agree': 15, 'Disagree': 13} , 
    {'Source': 'The Blaze', 'Bias': 'Right', 'Agree': 122955, 'Disagree': 92471} , 
    {'Source': 'The Block Charlotte', 'Bias': 'Lean Left', 'Agree': 6, 'Disagree': 6} , 
    {'Source': 'The Boston Globe', 'Bias': 'Left', 'Agree': 2022, 'Disagree': 1457} , 
    {'Source': 'The Bradford Era', 'Bias': 'Center', 'Agree': 10, 'Disagree': 11} , 
    {'Source': 'The Brazilian Report', 'Bias': 'Center', 'Agree': 33, 'Disagree': 28} , 
    {'Source': 'The Buffalo News', 'Bias': 'Center', 'Agree': 21, 'Disagree': 36} , 
    {'Source': 'The Bulwark', 'Bias': 'Lean Right', 'Agree': 268, 'Disagree': 362} , 
    {'Source': 'The Business Journals Denver', 'Bias': 'Center', 'Agree': 12, 'Disagree': 10} , 
    {'Source': 'The Business Times', 'Bias': 'Center', 'Agree': 9, 'Disagree': 10} , 
    {'Source': 'The Cadiz Record', 'Bias': 'Lean Left', 'Agree': 216, 'Disagree': 221} , 
    {'Source': 'The Californian', 'Bias': 'Center', 'Agree': 25, 'Disagree': 21} , 
    {'Source': 'The Canyon County Zephyr', 'Bias': 'Left', 'Agree': 238, 'Disagree': 180} , 
    {'Source': 'The Carolina Journal', 'Bias': 'Lean Right', 'Agree': 15, 'Disagree': 12} , 
    {'Source': 'The Catalyst', 'Bias': 'Lean Right', 'Agree': 48, 'Disagree': 55} , 
    {'Source': 'The Center for American Progress', 'Bias': 'Lean Left', 'Agree': 68, 'Disagree': 118} , 
    {'Source': 'The Center Square', 'Bias': 'Center', 'Agree': 45, 'Disagree': 52} , 
    {'Source': 'The Center Square - Michigan', 'Bias': 'Center', 'Agree': 146, 'Disagree': 239} , 
    {'Source': 'The Center Square - Minnesota', 'Bias': 'Center', 'Agree': 19, 'Disagree': 16} , 
    {'Source': 'The Center Square - Texas', 'Bias': 'Center', 'Agree': 22, 'Disagree': 18} , 
    {'Source': 'The Charlotte Post', 'Bias': 'Lean Left', 'Agree': 8, 'Disagree': 11} , 
    {'Source': 'The Cheyenne Post', 'Bias': 'Center', 'Agree': 8, 'Disagree': 8} , 
    {'Source': 'The Christian Century', 'Bias': 'Lean Left', 'Agree': 18, 'Disagree': 19} , 
    {'Source': 'The Christian Left Blog', 'Bias': 'Left', 'Agree': 21, 'Disagree': 20} , 
    {'Source': 'The Christian Post', 'Bias': 'Lean Right', 'Agree': 88, 'Disagree': 94} , 
    {'Source': 'The City', 'Bias': 'Lean Left', 'Agree': 14, 'Disagree': 16} , 
    {'Source': 'The Clarion-Ledger', 'Bias': 'Center', 'Agree': 37, 'Disagree': 39} , 
    {'Source': 'The Colebrook Chronicle', 'Bias': 'Center', 'Agree': 7, 'Disagree': 11} , 
    {'Source': 'The College Fix', 'Bias': 'Right', 'Agree': 334, 'Disagree': 266} , 
    {'Source': 'The Colorado Sun', 'Bias': 'Lean Left', 'Agree': 102, 'Disagree': 106} , 
    {'Source': 'The Columbian', 'Bias': 'Center', 'Agree': 23, 'Disagree': 21} , 
    {'Source': 'The Columbus Dispatch', 'Bias': 'Center', 'Agree': 93, 'Disagree': 137} , 
    {'Source': 'The Commercial Appeal', 'Bias': 'Lean Left', 'Agree': 235, 'Disagree': 289} , 
    {'Source': 'The Connection Newspapers', 'Bias': 'Center', 'Agree': 6, 'Disagree': 6} , 
    {'Source': 'The Conscious Conservative', 'Bias': 'Right', 'Agree': 19, 'Disagree': 28} , 
    {'Source': 'The Conversation', 'Bias': 'Lean Left', 'Agree': 492, 'Disagree': 371} , 
    {'Source': 'The Corpus Christi Caller-Times', 'Bias': 'Center', 'Agree': 23, 'Disagree': 24} , 
    {'Source': 'The Courier-Journal', 'Bias': 'Lean Left', 'Agree': 321, 'Disagree': 404} , 
    {'Source': 'The Courier-Tribune', 'Bias': 'Center', 'Agree': 11, 'Disagree': 12} , 
    {'Source': 'The Cradle', 'Bias': 'Lean Left', 'Agree': 90, 'Disagree': 113} , 
    {'Source': 'The Cross Timbers Gazette', 'Bias': 'Center', 'Agree': 8, 'Disagree': 8} , 
    {'Source': 'The Current', 'Bias': 'Center', 'Agree': 8, 'Disagree': 9} , 
    {'Source': 'The Daily Advance', 'Bias': 'Center', 'Agree': 44, 'Disagree': 55} , 
    {'Source': 'The Daily Caller', 'Bias': 'Right', 'Agree': 11685, 'Disagree': 4720} , 
    {'Source': 'The Daily Dot', 'Bias': 'Lean Left', 'Agree': 279, 'Disagree': 238} , 
    {'Source': 'The Daily Herald', 'Bias': 'Center', 'Agree': 21, 'Disagree': 30} , 
    {'Source': 'The Daily Iberian', 'Bias': 'Center', 'Agree': 11, 'Disagree': 13} , 
    {'Source': 'The Daily Iowan', 'Bias': 'Center', 'Agree': 27, 'Disagree': 34} , 
    {'Source': 'The Daily Nebraskan', 'Bias': 'Center', 'Agree': 13, 'Disagree': 12} , 
    {'Source': 'The Daily News Newburyport', 'Bias': 'Center', 'Agree': 15, 'Disagree': 17} , 
    {'Source': 'The Daily Nonpareil', 'Bias': 'Center', 'Agree': 12, 'Disagree': 18} , 
    {'Source': 'The Daily Signal', 'Bias': 'Right', 'Agree': 822, 'Disagree': 334} , 
    {'Source': 'The Daily Wire', 'Bias': 'Right', 'Agree': 14793, 'Disagree': 5075} , 
    {'Source': 'The Daily Yonder', 'Bias': 'Center', 'Agree': 36, 'Disagree': 46} , 
    {'Source': 'The Dakotan', 'Bias': 'Lean Right', 'Agree': 9, 'Disagree': 13} , 
    {'Source': 'The Dallas Morning News', 'Bias': 'Center', 'Agree': 350, 'Disagree': 426} , 
    {'Source': 'The Day', 'Bias': 'Center', 'Agree': 18, 'Disagree': 17} , 
    {'Source': 'The Deerfield Valley News', 'Bias': 'Center', 'Agree': 6, 'Disagree': 8} , 
    {'Source': 'The Delaware County Daily Times', 'Bias': 'Lean Left', 'Agree': 262, 'Disagree': 299} , 
    {'Source': 'The Delaware Wave', 'Bias': 'Center', 'Agree': 14, 'Disagree': 15} , 
    {'Source': 'The Denver Gazette', 'Bias': 'Center', 'Agree': 24, 'Disagree': 36} , 
    {'Source': 'The Denver North Star', 'Bias': 'Center', 'Agree': 12, 'Disagree': 15} , 
    {'Source': 'The Denver Post', 'Bias': 'Center', 'Agree': 225, 'Disagree': 228} , 
    {'Source': 'The Derrick', 'Bias': 'Center', 'Agree': 13, 'Disagree': 13} , 
    {'Source': 'The Dispatch', 'Bias': 'Lean Right', 'Agree': 477, 'Disagree': 298} , 
    {'Source': 'The East Valley Tribune', 'Bias': 'Center', 'Agree': 8, 'Disagree': 10} , 
    {'Source': 'The Eastern New Mexico News', 'Bias': 'Center', 'Agree': 5, 'Disagree': 4} , 
    {'Source': 'The Economist', 'Bias': 'Lean Left', 'Agree': 7791, 'Disagree': 13046} , 
    {'Source': 'The Ellsworth American', 'Bias': 'Center', 'Agree': 12, 'Disagree': 13} , 
    {'Source': 'The Epoch Times', 'Bias': 'Lean Right', 'Agree': 15455, 'Disagree': 9485} , 
    {'Source': 'The Federalist', 'Bias': 'Right', 'Agree': 11014, 'Disagree': 3511} , 
    {'Source': 'The Flip Side', 'Bias': 'Mixed', 'Agree': 602, 'Disagree': 422} , 
    {'Source': 'The Florida Capital Star', 'Bias': 'Right', 'Agree': 36, 'Disagree': 65} , 
    {'Source': 'The Forum of Fargo-Moorhead', 'Bias': 'Center', 'Agree': 20, 'Disagree': 18} , 
    {'Source': 'The Forward', 'Bias': 'Center', 'Agree': 15, 'Disagree': 42} , 
    {'Source': 'The Free Lance–Star', 'Bias': 'Center', 'Agree': 15, 'Disagree': 15} , 
    {'Source': 'The Free Press', 'Bias': 'Center', 'Agree': 239, 'Disagree': 217} , 
    {'Source': 'The Freestone County Times', 'Bias': 'Center', 'Agree': 8, 'Disagree': 8} , 
    {'Source': 'The Fulcrum', 'Bias': 'Center', 'Agree': 247, 'Disagree': 259} , 
    {'Source': 'The Garden Island', 'Bias': 'Center', 'Agree': 12, 'Disagree': 10} , 
    {'Source': 'The Gateway Pundit', 'Bias': 'Right', 'Agree': 1273, 'Disagree': 623} , 
    {'Source': 'The Georgia Star News', 'Bias': 'Right', 'Agree': 39, 'Disagree': 56} , 
    {'Source': 'The Georgia Sun', 'Bias': 'Center', 'Agree': 17, 'Disagree': 15} , 
    {'Source': 'The Georgia Virtue', 'Bias': 'Center', 'Agree': 8, 'Disagree': 7} , 
    {'Source': 'The Gilmer Mirror', 'Bias': 'Center', 'Agree': 9, 'Disagree': 12} , 
    {'Source': 'The Globe and Mail', 'Bias': 'Center', 'Agree': 346, 'Disagree': 475} , 
    {'Source': 'The Grio', 'Bias': 'Lean Left', 'Agree': 38, 'Disagree': 30} , 
    {'Source': 'The Guardian', 'Bias': 'Lean Left', 'Agree': 18447, 'Disagree': 11956} , 
    {'Source': 'The Hankyoreh', 'Bias': 'Left', 'Agree': 12, 'Disagree': 8} , 
    {'Source': 'The Hardwood Institiute', 'Bias': 'Center', 'Agree': 10, 'Disagree': 11} , 
    {'Source': 'The Herald Banner', 'Bias': 'Center', 'Agree': 11, 'Disagree': 11} , 
    {'Source': 'The Herald Bulletin', 'Bias': 'Center', 'Agree': 14, 'Disagree': 12} , 
    {'Source': 'The Herald News', 'Bias': 'Center', 'Agree': 11, 'Disagree': 11} , 
    {'Source': 'The Heritage Foundation', 'Bias': 'Lean Right', 'Agree': 3461, 'Disagree': 2005} , 
    {'Source': 'The HighWire', 'Bias': 'Lean Right', 'Agree': 24, 'Disagree': 31} , 
    {'Source': 'The Hill', 'Bias': 'Center', 'Agree': 20595, 'Disagree': 28608} , 
    {'Source': 'The Hollywood Reporter', 'Bias': 'Lean Left', 'Agree': 133, 'Disagree': 147} , 
    {'Source': 'The Huntsville Item', 'Bias': 'Center', 'Agree': 29, 'Disagree': 24} , 
    {'Source': 'The Hutchinson News', 'Bias': 'Center', 'Agree': 11, 'Disagree': 14} , 
    {'Source': 'The Imaginative Conservative', 'Bias': 'Right', 'Agree': 162, 'Disagree': 115} , 
    {'Source': 'The Independent', 'Bias': 'Lean Left', 'Agree': 1006, 'Disagree': 757} , 
    {'Source': 'The Indiana Gazette', 'Bias': 'Center', 'Agree': 9, 'Disagree': 10} , 
    {'Source': 'The Intercept', 'Bias': 'Left', 'Agree': 6916, 'Disagree': 2289} , 
    {'Source': 'The Iowa Torch', 'Bias': 'Lean Right', 'Agree': 29, 'Disagree': 24} , 
    {'Source': 'The Irish Times', 'Bias': 'Center', 'Agree': 46, 'Disagree': 49} , 
    {'Source': 'The Jackson Sun', 'Bias': 'Center', 'Agree': 10, 'Disagree': 8} , 
    {'Source': 'The Japan Times', 'Bias': 'Center', 'Agree': 134, 'Disagree': 122} , 
    {'Source': 'The Jerusalem Post', 'Bias': 'Center', 'Agree': 466, 'Disagree': 524} , 
    {'Source': 'The Jolt News Organization', 'Bias': 'Center', 'Agree': 7, 'Disagree': 9} , 
    {'Source': 'The Joplin Globe', 'Bias': 'Center', 'Agree': 8, 'Disagree': 6} , 
    {'Source': 'The Journal Gazette', 'Bias': 'Center', 'Agree': 16, 'Disagree': 18} , 
    {'Source': 'The Journal of the San Juan Islands', 'Bias': 'Center', 'Agree': 13, 'Disagree': 19} , 
    {'Source': 'The Journal Times', 'Bias': 'Center', 'Agree': 17, 'Disagree': 20} , 
    {'Source': 'The Juggernaut', 'Bias': 'Left', 'Agree': 65, 'Disagree': 41} , 
    {'Source': 'The Justice', 'Bias': 'Lean Left', 'Agree': 201, 'Disagree': 217} , 
    {'Source': 'The Kansas City Beacon', 'Bias': 'Center', 'Agree': 10, 'Disagree': 12} , 
    {'Source': 'The Kansas City Star', 'Bias': 'Center', 'Agree': 20, 'Disagree': 42} , 
    {'Source': 'The Kansas City Star', 'Bias': 'Center', 'Agree': 18, 'Disagree': 28} , 
    {'Source': 'The Kentucky Daily', 'Bias': 'Center', 'Agree': 5, 'Disagree': 7} , 
    {'Source': 'The Korea Herald', 'Bias': 'Center', 'Agree': 270, 'Disagree': 212} , 
    {'Source': 'The Kyiv Independent', 'Bias': 'Center', 'Agree': 81, 'Disagree': 75} , 
    {'Source': 'The Leaf-Chronicle', 'Bias': 'Center', 'Agree': 15, 'Disagree': 13} , 
    {'Source': 'The Libertarian Republic', 'Bias': 'Lean Right', 'Agree': 937, 'Disagree': 803} , 
    {'Source': 'The Lincoln County News', 'Bias': 'Center', 'Agree': 8, 'Disagree': 7} , 
    {'Source': 'The Lincoln Project', 'Bias': 'Mixed', 'Agree': 81, 'Disagree': 347} , 
    {'Source': 'The Louisiana Weekly', 'Bias': 'Center', 'Agree': 4, 'Disagree': 7} , 
    {'Source': 'The Lowndes Signal', 'Bias': 'Center', 'Agree': 9, 'Disagree': 11} , 
    {'Source': 'The Lufkin Daily News', 'Bias': 'Center', 'Agree': 48, 'Disagree': 46} , 
    {'Source': 'The Maine Monitor', 'Bias': 'Lean Left', 'Agree': 11, 'Disagree': 15} , 
    {'Source': 'The Maine Wire', 'Bias': 'Right', 'Agree': 91, 'Disagree': 46} , 
    {'Source': 'The Maneater', 'Bias': 'Lean Left', 'Agree': 57, 'Disagree': 54} , 
    {'Source': 'The Manila Times', 'Bias': 'Center', 'Agree': 16, 'Disagree': 20} , 
    {'Source': 'The Marietta Times', 'Bias': 'Center', 'Agree': 11, 'Disagree': 10} , 
    {'Source': 'The Markup', 'Bias': 'Center', 'Agree': 44, 'Disagree': 60} , 
    {'Source': 'The Marshall News Messenger', 'Bias': 'Center', 'Agree': 9, 'Disagree': 8} , 
    {'Source': 'The Marshall Project', 'Bias': 'Center', 'Agree': 106, 'Disagree': 162} , 
    {'Source': "The Martha's Vineyard Times", 'Bias': 'Center', 'Agree': 6, 'Disagree': 7} , 
    {'Source': 'The Maui News', 'Bias': 'Center', 'Agree': 20, 'Disagree': 20} , 
    {'Source': 'The McLeod County Chronicle', 'Bias': 'Center', 'Agree': 8, 'Disagree': 14} , 
    {'Source': 'The Messenger', 'Bias': 'Center', 'Agree': 143, 'Disagree': 137} , 
    {'Source': 'The Michigan Star', 'Bias': 'Right', 'Agree': 23, 'Disagree': 45} , 
    {'Source': 'The Middletown Press', 'Bias': 'Lean Left', 'Agree': 14, 'Disagree': 13} , 
    {'Source': 'The Minnesota Daily', 'Bias': 'Lean Left', 'Agree': 13, 'Disagree': 15} , 
    {'Source': 'The Minority Eye', 'Bias': 'Left', 'Agree': 32, 'Disagree': 17} , 
    {'Source': 'The Mirror', 'Bias': 'Left', 'Agree': 8, 'Disagree': 3} , 
    {'Source': 'The Mississippi Link', 'Bias': 'Lean Left', 'Agree': 5, 'Disagree': 7} , 
    {'Source': 'The Mon Valley Independent', 'Bias': 'Center', 'Agree': 7, 'Disagree': 7} , 
    {'Source': 'The Monmouth Journal Eastern', 'Bias': 'Center', 'Agree': 6, 'Disagree': 6} , 
    {'Source': 'The Montana Standard', 'Bias': 'Center', 'Agree': 19, 'Disagree': 20} , 
    {'Source': 'The Narratives Project', 'Bias': 'Center', 'Agree': 14, 'Disagree': 14} , 
    {'Source': 'The Nation', 'Bias': 'Left', 'Agree': 2038, 'Disagree': 615} , 
    {'Source': 'The National Pulse', 'Bias': 'Right', 'Agree': 653, 'Disagree': 182} , 
    {'Source': 'The Nevada Globe', 'Bias': 'Lean Right', 'Agree': 6, 'Disagree': 8} , 
    {'Source': 'The Nevada Independent', 'Bias': 'Center', 'Agree': 9, 'Disagree': 12} , 
    {'Source': 'The Nevada Independent', 'Bias': 'Center', 'Agree': 42, 'Disagree': 52} , 
    {'Source': 'The New Orleans Advocate', 'Bias': 'Center', 'Agree': 12, 'Disagree': 15} , 
    {'Source': 'The New York Sun', 'Bias': 'Right', 'Agree': 45, 'Disagree': 57} , 
    {'Source': 'The New Yorker', 'Bias': 'Left', 'Agree': 11758, 'Disagree': 2997} , 
    {'Source': 'The Newport Daily News', 'Bias': 'Center', 'Agree': 17, 'Disagree': 16} , 
    {'Source': 'The News & Observer', 'Bias': 'Center', 'Agree': 88, 'Disagree': 126} , 
    {'Source': 'The News Journal', 'Bias': 'Center', 'Agree': 17, 'Disagree': 15} , 
    {'Source': 'The News Tribune', 'Bias': 'Center', 'Agree': 20, 'Disagree': 17} , 
    {'Source': 'The News-Herald', 'Bias': 'Center', 'Agree': 10, 'Disagree': 12} , 
    {'Source': 'The Nome Nugget', 'Bias': 'Center', 'Agree': 10, 'Disagree': 14} , 
    {'Source': 'The Northern Virginia Daily', 'Bias': 'Center', 'Agree': 12, 'Disagree': 14} , 
    {'Source': 'The Oaklandside', 'Bias': 'Center', 'Agree': 6, 'Disagree': 9} , 
    {'Source': 'The Observer', 'Bias': 'Center', 'Agree': 10, 'Disagree': 11} , 
    {'Source': 'The Observer (New York)', 'Bias': 'Center', 'Agree': 306, 'Disagree': 531} , 
    {'Source': 'The Oklahoman', 'Bias': 'Center', 'Agree': 24, 'Disagree': 24} , 
    {'Source': 'The Olympian', 'Bias': 'Center', 'Agree': 17, 'Disagree': 15} , 
    {'Source': 'The Onion (Humor)', 'Bias': 'Lean Left', 'Agree': 732, 'Disagree': 413} , 
    {'Source': 'The Oracle', 'Bias': 'Center', 'Agree': 155, 'Disagree': 188} , 
    {'Source': 'The Oregonian', 'Bias': 'Center', 'Agree': 129, 'Disagree': 254} , 
    {'Source': 'The Palm Beach Post', 'Bias': 'Center', 'Agree': 34, 'Disagree': 34} , 
    {'Source': 'The Pantagraph', 'Bias': 'Center', 'Agree': 15, 'Disagree': 15} , 
    {'Source': 'The Patriot Ledger', 'Bias': 'Center', 'Agree': 21, 'Disagree': 19} , 
    {'Source': 'The Patriot Post', 'Bias': 'Right', 'Agree': 102, 'Disagree': 143} , 
    {'Source': 'The Patriot-News', 'Bias': 'Center', 'Agree': 35, 'Disagree': 52} , 
    {'Source': 'The Penobscot Times', 'Bias': 'Center', 'Agree': 7, 'Disagree': 9} , 
    {'Source': 'The Philadelphia Inquirer', 'Bias': 'Lean Left', 'Agree': 378, 'Disagree': 379} , 
    {'Source': 'The Philadelphia Sunday Sun', 'Bias': 'Center', 'Agree': 11, 'Disagree': 11} , 
    {'Source': 'The Philly Tribune', 'Bias': 'Left', 'Agree': 35, 'Disagree': 19} , 
    {'Source': 'The Plain Dealer', 'Bias': 'Center', 'Agree': 11, 'Disagree': 15} , 
    {'Source': 'The Police Tribune', 'Bias': 'Lean Right', 'Agree': 111, 'Disagree': 91} , 
    {'Source': 'The Portsmouth Herald', 'Bias': 'Center', 'Agree': 31, 'Disagree': 29} , 
    {'Source': 'The Post and Courier', 'Bias': 'Lean Right', 'Agree': 32, 'Disagree': 28} , 
    {'Source': 'The Post Millennial', 'Bias': 'Right', 'Agree': 516, 'Disagree': 391} , 
    {'Source': 'The Post-Star', 'Bias': 'Center', 'Agree': 15, 'Disagree': 20} , 
    {'Source': 'The Presbyterian Outlook', 'Bias': 'Lean Left', 'Agree': 7, 'Disagree': 12} , 
    {'Source': 'The Prescott Times', 'Bias': 'Center', 'Agree': 11, 'Disagree': 11} , 
    {'Source': 'The Press of Atlantic City', 'Bias': 'Center', 'Agree': 23, 'Disagree': 25} , 
    {'Source': 'The Press-Enterprise', 'Bias': 'Lean Right', 'Agree': 60, 'Disagree': 55} , 
    {'Source': 'The Problem Solvers Caucus', 'Bias': 'Center', 'Agree': 20, 'Disagree': 16} , 
    {'Source': 'The Providence Journal', 'Bias': 'Center', 'Agree': 22, 'Disagree': 20} , 
    {'Source': 'The Provincetown Independent', 'Bias': 'Center', 'Agree': 11, 'Disagree': 10} , 
    {'Source': 'The Rachel Maddow Show', 'Bias': 'Left', 'Agree': 85, 'Disagree': 32} , 
    {'Source': 'The Reading Eagle', 'Bias': 'Center', 'Agree': 8, 'Disagree': 12} , 
    {'Source': 'The Red and Black', 'Bias': 'Center', 'Agree': 247, 'Disagree': 185} , 
    {'Source': 'The Register-Guard', 'Bias': 'Center', 'Agree': 17, 'Disagree': 17} , 
    {'Source': 'The Reliable Bias', 'Bias': 'Center', 'Agree': 189, 'Disagree': 217} , 
    {'Source': 'The Reno Gazette-Journal', 'Bias': 'Lean Left', 'Agree': 33, 'Disagree': 32} , 
    {'Source': 'The Reporters Committee for Freedom of the Press', 'Bias': 'Center', 'Agree': 73, 'Disagree': 60} , 
    {'Source': 'The Republic News', 'Bias': 'Center', 'Agree': 17, 'Disagree': 17} , 
    {'Source': 'The Republican', 'Bias': 'Center', 'Agree': 286, 'Disagree': 572} , 
    {'Source': 'The Republican Journal', 'Bias': 'Lean Right', 'Agree': 28, 'Disagree': 28} , 
    {'Source': 'The Resurgent', 'Bias': 'Right', 'Agree': 194, 'Disagree': 184} , 
    {'Source': 'The Richfield Reaper', 'Bias': 'Center', 'Agree': 9, 'Disagree': 10} , 
    {'Source': 'The Ripon Advance', 'Bias': 'Lean Right', 'Agree': 30, 'Disagree': 29} , 
    {'Source': 'The Roanoke Times', 'Bias': 'Center', 'Agree': 19, 'Disagree': 26} , 
    {'Source': 'The Root', 'Bias': 'Lean Left', 'Agree': 536, 'Disagree': 694} , 
    {'Source': 'The Sacramento Bee', 'Bias': 'Lean Left', 'Agree': 429, 'Disagree': 527} , 
    {'Source': 'The Salt Lake Tribune', 'Bias': 'Lean Left', 'Agree': 84, 'Disagree': 79} , 
    {'Source': 'The San Francisco Standard', 'Bias': 'Center', 'Agree': 20, 'Disagree': 26} , 
    {'Source': 'The Saturday Evening Post', 'Bias': 'Center', 'Agree': 282, 'Disagree': 227} , 
    {'Source': 'The Seattle Times', 'Bias': 'Center', 'Agree': 341, 'Disagree': 642} , 
    {'Source': 'The Sierra Club', 'Bias': 'Lean Left', 'Agree': 230, 'Disagree': 346} , 
    {'Source': 'The South African', 'Bias': 'Center', 'Agree': 49, 'Disagree': 46} , 
    {'Source': 'The Southern Maryland Chronicle', 'Bias': 'Lean Left', 'Agree': 4, 'Disagree': 8} , 
    {'Source': 'The Spectator World', 'Bias': 'Right', 'Agree': 306, 'Disagree': 218} , 
    {'Source': 'The State', 'Bias': 'Lean Right', 'Agree': 11, 'Disagree': 18} , 
    {'Source': 'The State', 'Bias': 'Center', 'Agree': 7, 'Disagree': 6} , 
    {'Source': 'The State', 'Bias': 'Center', 'Agree': 40, 'Disagree': 37} , 
    {'Source': 'The State Journal-Register', 'Bias': 'Center', 'Agree': 15, 'Disagree': 14} , 
    {'Source': 'The Steamboat Institute', 'Bias': 'Lean Right', 'Agree': 27, 'Disagree': 24} , 
    {'Source': 'The Sun', 'Bias': 'Center', 'Agree': 31, 'Disagree': 72} , 
    {'Source': 'The Sun News', 'Bias': 'Center', 'Agree': 38, 'Disagree': 64} , 
    {'Source': 'The Telegraph - UK', 'Bias': 'Lean Right', 'Agree': 2635, 'Disagree': 1177} , 
    {'Source': 'The Tennessean', 'Bias': 'Center', 'Agree': 85, 'Disagree': 94} , 
    {'Source': 'The Texan', 'Bias': 'Lean Right', 'Agree': 241, 'Disagree': 186} , 
    {'Source': 'The Texas Observer', 'Bias': 'Lean Left', 'Agree': 132, 'Disagree': 115} , 
    {'Source': 'The Texas Tribune', 'Bias': 'Lean Left', 'Agree': 964, 'Disagree': 474} , 
    {'Source': 'The Thread', 'Bias': 'Mixed', 'Agree': 107, 'Disagree': 115} , 
    {'Source': 'The Times', 'Bias': 'Center', 'Agree': 99, 'Disagree': 154} , 
    {'Source': 'The Times and Democrat', 'Bias': 'Center', 'Agree': 17, 'Disagree': 22} , 
    {'Source': 'The Times Herald', 'Bias': 'Center', 'Agree': 15, 'Disagree': 16} , 
    {'Source': 'The Times of Israel', 'Bias': 'Center', 'Agree': 163, 'Disagree': 227} , 
    {'Source': 'The Times of Northwest Indiana', 'Bias': 'Center', 'Agree': 17, 'Disagree': 18} , 
    {'Source': 'The Times of Northwest Indiana', 'Bias': 'Center', 'Agree': 12, 'Disagree': 19} , 
    {'Source': 'The Times-Independent', 'Bias': 'Center', 'Agree': 9, 'Disagree': 13} , 
    {'Source': 'The Times-Picayune', 'Bias': 'Center', 'Agree': 60, 'Disagree': 109} , 
    {'Source': 'The TimesDaily', 'Bias': 'Center', 'Agree': 16, 'Disagree': 15} , 
    {'Source': 'The Topeka Capital-Journal', 'Bias': 'Center', 'Agree': 14, 'Disagree': 20} , 
    {'Source': 'The Topeka Capital-Journal', 'Bias': 'Center', 'Agree': 16, 'Disagree': 17} , 
    {'Source': 'The Trentonian', 'Bias': 'Center', 'Agree': 18, 'Disagree': 24} , 
    {'Source': 'The Triton', 'Bias': 'Center', 'Agree': 9, 'Disagree': 9} , 
    {'Source': 'The Verge', 'Bias': 'Lean Left', 'Agree': 1136, 'Disagree': 740} , 
    {'Source': 'The Vindicator', 'Bias': 'Center', 'Agree': 21, 'Disagree': 20} , 
    {'Source': 'The Virginia Gazette', 'Bias': 'Center', 'Agree': 10, 'Disagree': 12} , 
    {'Source': 'The Virginian-Pilot', 'Bias': 'Center', 'Agree': 18, 'Disagree': 30} , 
    {'Source': 'The Walsh County Record', 'Bias': 'Center', 'Agree': 12, 'Disagree': 14} , 
    {'Source': 'The Washington Informer', 'Bias': 'Lean Left', 'Agree': 17, 'Disagree': 18} , 
    {'Source': 'The Washington Sun', 'Bias': 'Center', 'Agree': 7, 'Disagree': 10} , 
    {'Source': 'The Week - News', 'Bias': 'Lean Left', 'Agree': 4241, 'Disagree': 3471} , 
    {'Source': 'The Week - Opinion', 'Bias': 'Lean Left', 'Agree': 276, 'Disagree': 242} , 
    {'Source': 'The Weekly Packet', 'Bias': 'Center', 'Agree': 9, 'Disagree': 11} , 
    {'Source': 'The Weekly Standard', 'Bias': 'Right', 'Agree': 1429, 'Disagree': 882} , 
    {'Source': 'The Weirton Daily Times', 'Bias': 'Center', 'Agree': 24, 'Disagree': 27} , 
    {'Source': 'The Westerly Sun', 'Bias': 'Center', 'Agree': 13, 'Disagree': 12} , 
    {'Source': 'The Western Journal', 'Bias': 'Right', 'Agree': 2024, 'Disagree': 650} , 
    {'Source': 'The Wichita Eagle', 'Bias': 'Center', 'Agree': 16, 'Disagree': 19} , 
    {'Source': 'The Winchester Star', 'Bias': 'Center', 'Agree': 9, 'Disagree': 8} , 
    {'Source': 'The World Link', 'Bias': 'Center', 'Agree': 12, 'Disagree': 10} , 
    {'Source': 'The Wyoming Tribune Eagle', 'Bias': 'Center', 'Agree': 40, 'Disagree': 42} , 
    {'Source': 'The Young Turks', 'Bias': 'Left', 'Agree': 339, 'Disagree': 74} , 
    {'Source': 'TheGailyGrind', 'Bias': 'Left', 'Agree': 29, 'Disagree': 14} , 
    {'Source': 'Them', 'Bias': 'Lean Left', 'Agree': 32, 'Disagree': 29} , 
    {'Source': 'theSkimm', 'Bias': 'Lean Left', 'Agree': 31, 'Disagree': 26} , 
    {'Source': 'ThinkProgress', 'Bias': 'Left', 'Agree': 2849, 'Disagree': 990} , 
    {'Source': 'This Week in Worcester', 'Bias': 'Center', 'Agree': 10, 'Disagree': 11} , 
    {'Source': 'Thomas B. Edsall', 'Bias': 'Lean Left', 'Agree': 30, 'Disagree': 39} , 
    {'Source': 'Thomas Franck', 'Bias': 'Center', 'Agree': 23, 'Disagree': 19} , 
    {'Source': 'Thomas Frank', 'Bias': 'Lean Left', 'Agree': 198, 'Disagree': 206} , 
    {'Source': 'Thomas L. Friedman', 'Bias': 'Lean Left', 'Agree': 138, 'Disagree': 188} , 
    {'Source': 'Thomas Sowell', 'Bias': 'Lean Right', 'Agree': 640, 'Disagree': 426} , 
    {'Source': 'THV11', 'Bias': 'Center', 'Agree': 22, 'Disagree': 21} , 
    {'Source': 'Tiana Lowe Doescher', 'Bias': 'Right', 'Agree': 46, 'Disagree': 57} , 
    {'Source': 'Tiffin Ohio News', 'Bias': 'Lean Left', 'Agree': 6, 'Disagree': 7} , 
    {'Source': 'Tim Groseclose', 'Bias': 'Lean Right', 'Agree': 126, 'Disagree': 97} , 
    {'Source': 'Tim Pool', 'Bias': 'Center', 'Agree': 2011, 'Disagree': 2914} , 
    {'Source': 'Tim Scott', 'Bias': 'Lean Right', 'Agree': 22, 'Disagree': 32} , 
    {'Source': 'Timber Lake Topic', 'Bias': 'Center', 'Agree': 8, 'Disagree': 9} , 
    {'Source': 'Time Magazine', 'Bias': 'Lean Left', 'Agree': 10939, 'Disagree': 9397} , 
    {'Source': 'Times Argus', 'Bias': 'Center', 'Agree': 11, 'Disagree': 15} , 
    {'Source': 'Times Leader', 'Bias': 'Center', 'Agree': 14, 'Disagree': 16} , 
    {'Source': 'Times Standard', 'Bias': 'Center', 'Agree': 7, 'Disagree': 10} , 
    {'Source': 'Times Union', 'Bias': 'Center', 'Agree': 55, 'Disagree': 57} , 
    {'Source': 'Times-Georgian', 'Bias': 'Center', 'Agree': 7, 'Disagree': 9} , 
    {'Source': "Timothy L. O'Brien", 'Bias': 'Lean Left', 'Agree': 27, 'Disagree': 31} , 
    {'Source': 'Timothy P. Carney', 'Bias': 'Lean Right', 'Agree': 17, 'Disagree': 16} , 
    {'Source': 'Todays Chronic', 'Bias': 'Lean Left', 'Agree': 12, 'Disagree': 20} , 
    {'Source': 'Tom Cole', 'Bias': 'Right', 'Agree': 195, 'Disagree': 166} , 
    {'Source': 'Tom Nichols', 'Bias': 'Lean Right', 'Agree': 117, 'Disagree': 138} , 
    {'Source': 'Tom Rogan', 'Bias': 'Center', 'Agree': 19, 'Disagree': 30} , 
    {'Source': 'Tom Toles (cartoonist)', 'Bias': 'Left', 'Agree': 130, 'Disagree': 111} , 
    {'Source': 'Tony Auth (cartoonist)', 'Bias': 'Left', 'Agree': 93, 'Disagree': 70} , 
    {'Source': 'Tonya Russell', 'Bias': 'Lean Left', 'Agree': 53, 'Disagree': 48} , 
    {'Source': 'Toronto Star', 'Bias': 'Center', 'Agree': 166, 'Disagree': 387} , 
    {'Source': 'Town Square Deleware', 'Bias': 'Center', 'Agree': 16, 'Disagree': 23} , 
    {'Source': 'Townhall', 'Bias': 'Right', 'Agree': 10049, 'Disagree': 14262} , 
    {'Source': 'Trains.com', 'Bias': 'Center', 'Agree': 66, 'Disagree': 78} , 
    {'Source': 'Trans Writes', 'Bias': 'Lean Left', 'Agree': 22, 'Disagree': 30} , 
    {'Source': 'Tri-City Herald', 'Bias': 'Center', 'Agree': 12, 'Disagree': 14} , 
    {'Source': 'Truthdig', 'Bias': 'Left', 'Agree': 139, 'Disagree': 76} , 
    {'Source': 'TruthOut', 'Bias': 'Lean Left', 'Agree': 560, 'Disagree': 550} , 
    {'Source': 'Tucker Carlson', 'Bias': 'Right', 'Agree': 1192, 'Disagree': 433} , 
    {'Source': 'Tulsa World', 'Bias': 'Center', 'Agree': 42, 'Disagree': 40} , 
    {'Source': 'Turning Point USA', 'Bias': 'Right', 'Agree': 78, 'Disagree': 41} , 
    {'Source': 'Tuscaloosa News', 'Bias': 'Center', 'Agree': 19, 'Disagree': 19} , 
    {'Source': 'Twin Cities PBS', 'Bias': 'Center', 'Agree': 30, 'Disagree': 39} , 
    {'Source': 'Twin Cities Pioneer Press', 'Bias': 'Center', 'Agree': 25, 'Disagree': 33} , 
    {'Source': 'Twin City Times', 'Bias': 'Center', 'Agree': 8, 'Disagree': 10} , 
    {'Source': 'Tyler Morning Telegraph', 'Bias': 'Center', 'Agree': 13, 'Disagree': 14} , 
    {'Source': 'U.S. News & World Report', 'Bias': 'Lean Left', 'Agree': 2183, 'Disagree': 2230} , 
    {'Source': 'UnHerd', 'Bias': 'Center', 'Agree': 183, 'Disagree': 161} , 
    {'Source': 'United Methodist Insight', 'Bias': 'Left', 'Agree': 10, 'Disagree': 13} , 
    {'Source': 'United Methodist News', 'Bias': 'Lean Left', 'Agree': 10, 'Disagree': 12} , 
    {'Source': 'United Press International', 'Bias': 'Center', 'Agree': 68, 'Disagree': 43} , 
    {'Source': 'United States Courts', 'Bias': 'Center', 'Agree': 277, 'Disagree': 382} , 
    {'Source': 'Univision', 'Bias': 'Lean Left', 'Agree': 668, 'Disagree': 679} , 
    {'Source': 'Up North News Wisconsin', 'Bias': 'Lean Left', 'Agree': 11, 'Disagree': 13} , 
    {'Source': 'Upper Michigans Source', 'Bias': 'Center', 'Agree': 16, 'Disagree': 13} , 
    {'Source': 'Upward News', 'Bias': 'Lean Right', 'Agree': 172, 'Disagree': 118} , 
    {'Source': 'Upward News Editorial Team', 'Bias': 'Lean Right', 'Agree': 47, 'Disagree': 61} , 
    {'Source': 'Upworthy', 'Bias': 'Left', 'Agree': 580, 'Disagree': 389} , 
    {'Source': 'Urban Institute', 'Bias': 'Lean Left', 'Agree': 610, 'Disagree': 512} , 
    {'Source': 'USA TODAY', 'Bias': 'Lean Left', 'Agree': 20696, 'Disagree': 23283} , 
    {'Source': 'Valley News', 'Bias': 'Center', 'Agree': 36, 'Disagree': 42} , 
    {'Source': 'Valley News Live', 'Bias': 'Center', 'Agree': 12, 'Disagree': 10} , 
    {'Source': 'Vanderbilt Project on Unity and American Democracy', 'Bias': 'Center', 'Agree': 17, 'Disagree': 15} , 
    {'Source': 'Vanity Fair', 'Bias': 'Lean Left', 'Agree': 3979, 'Disagree': 2730} , 
    {'Source': 'Variety', 'Bias': 'Lean Left', 'Agree': 120, 'Disagree': 236} , 
    {'Source': 'Vatican News', 'Bias': 'Lean Right', 'Agree': 18, 'Disagree': 22} , 
    {'Source': 'Vermont Public', 'Bias': 'Center', 'Agree': 12, 'Disagree': 41} , 
    {'Source': 'Vermont Standard', 'Bias': 'Center', 'Agree': 12, 'Disagree': 14} , 
    {'Source': 'Vice', 'Bias': 'Left', 'Agree': 5120, 'Disagree': 1217} , 
    {'Source': 'Victor Hanson', 'Bias': 'Lean Right', 'Agree': 299, 'Disagree': 308} , 
    {'Source': 'Virginia Business', 'Bias': 'Center', 'Agree': 13, 'Disagree': 11} , 
    {'Source': 'Virginia Center for Investigative Journalism', 'Bias': 'Lean Left', 'Agree': 13, 'Disagree': 14} , 
    {'Source': 'Virginia Mercury', 'Bias': 'Center', 'Agree': 92, 'Disagree': 98} , 
    {'Source': 'Virtue Online', 'Bias': 'Right', 'Agree': 12, 'Disagree': 25} , 
    {'Source': 'Vogue', 'Bias': 'Left', 'Agree': 61, 'Disagree': 35} , 
    {'Source': 'Voice of America (VOA)', 'Bias': 'Center', 'Agree': 343, 'Disagree': 373} , 
    {'Source': 'Voice of Chid (Chidike Okeem)', 'Bias': 'Right', 'Agree': 12, 'Disagree': 21} , 
    {'Source': 'Volante', 'Bias': 'Center', 'Agree': 198, 'Disagree': 219} , 
    {'Source': 'Vote Smart', 'Bias': 'Center', 'Agree': 281, 'Disagree': 280} , 
    {'Source': 'Votebeat', 'Bias': 'Center', 'Agree': 7, 'Disagree': 14} , 
    {'Source': 'Votebeat Arizona', 'Bias': 'Center', 'Agree': 4, 'Disagree': 6} , 
    {'Source': 'Vox', 'Bias': 'Left', 'Agree': 34943, 'Disagree': 15943} , 
    {'Source': 'VT Digger', 'Bias': 'Center', 'Agree': 265, 'Disagree': 292} , 
    {'Source': 'WABI 5', 'Bias': 'Center', 'Agree': 9, 'Disagree': 7} , 
    {'Source': 'Waco Tribune-Herald', 'Bias': 'Center', 'Agree': 11, 'Disagree': 13} , 
    {'Source': 'WAFB 9', 'Bias': 'Center', 'Agree': 9, 'Disagree': 12} , 
    {'Source': 'WAGM 8', 'Bias': 'Center', 'Agree': 4, 'Disagree': 5} , 
    {'Source': 'Wake Up to Politics', 'Bias': 'Center', 'Agree': 151, 'Disagree': 129} , 
    {'Source': 'Wall Street Journal (News)', 'Bias': 'Center', 'Agree': 28003, 'Disagree': 29757} , 
    {'Source': 'Wall Street Journal (Opinion)', 'Bias': 'Lean Right', 'Agree': 13141, 'Disagree': 8836} , 
    {'Source': 'Walt Handelsman (cartoonist)', 'Bias': 'Left', 'Agree': 140, 'Disagree': 140} , 
    {'Source': 'WANDTV', 'Bias': 'Center', 'Agree': 119, 'Disagree': 111} , 
    {'Source': 'WANE 15', 'Bias': 'Center', 'Agree': 11, 'Disagree': 11} , 
    {'Source': 'Washington Blade', 'Bias': 'Lean Left', 'Agree': 25, 'Disagree': 28} , 
    {'Source': 'Washington City Paper', 'Bias': 'Center', 'Agree': 14, 'Disagree': 18} , 
    {'Source': 'Washington County Insider', 'Bias': 'Center', 'Agree': 8, 'Disagree': 9} , 
    {'Source': 'Washington Diplomat', 'Bias': 'Center', 'Agree': 9, 'Disagree': 12} , 
    {'Source': 'Washington Examiner', 'Bias': 'Lean Right', 'Agree': 15949, 'Disagree': 8181} , 
    {'Source': 'Washington Free Beacon', 'Bias': 'Right', 'Agree': 1355, 'Disagree': 875} , 
    {'Source': 'Washington Monthly', 'Bias': 'Lean Left', 'Agree': 384, 'Disagree': 363} , 
    {'Source': 'Washington Post', 'Bias': 'Lean Left', 'Agree': 40953, 'Disagree': 30109} , 
    {'Source': 'Washington Times', 'Bias': 'Lean Right', 'Agree': 29853, 'Disagree': 14467} , 
    {'Source': 'Watchdog.org', 'Bias': 'Lean Right', 'Agree': 638, 'Disagree': 674} , 
    {'Source': 'WATD', 'Bias': 'Center', 'Agree': 9, 'Disagree': 10} , 
    {'Source': 'Watertown Public Opinion', 'Bias': 'Center', 'Agree': 13, 'Disagree': 23} , 
    {'Source': 'WBAL 11', 'Bias': 'Center', 'Agree': 13, 'Disagree': 14} , 
    {'Source': 'WBAY 2', 'Bias': 'Center', 'Agree': 14, 'Disagree': 13} , 
    {'Source': 'WBBJ 7 Eyewitness News', 'Bias': 'Center', 'Agree': 11, 'Disagree': 10} , 
    {'Source': 'WBIR 10', 'Bias': 'Center', 'Agree': 14, 'Disagree': 17} , 
    {'Source': 'WBKO 13', 'Bias': 'Center', 'Agree': 9, 'Disagree': 10} , 
    {'Source': 'WBOC Delaware', 'Bias': 'Center', 'Agree': 4, 'Disagree': 4} , 
    {'Source': 'WBOY 12', 'Bias': 'Center', 'Agree': 15, 'Disagree': 16} , 
    {'Source': 'WBUR', 'Bias': 'Center', 'Agree': 65, 'Disagree': 76} , 
    {'Source': 'WCAI', 'Bias': 'Lean Left', 'Agree': 6, 'Disagree': 8} , 
    {'Source': 'WCAX 3', 'Bias': 'Center', 'Agree': 15, 'Disagree': 13} , 
    {'Source': 'WCBD 2', 'Bias': 'Center', 'Agree': 6, 'Disagree': 4} , 
    {'Source': 'WCIA', 'Bias': 'Center', 'Agree': 14, 'Disagree': 15} , 
    {'Source': 'WCPO 9', 'Bias': 'Center', 'Agree': 14, 'Disagree': 14} , 
    {'Source': 'WCPT', 'Bias': 'Lean Left', 'Agree': 12, 'Disagree': 12} , 
    {'Source': 'WCVB', 'Bias': 'Center', 'Agree': 44, 'Disagree': 48} , 
    {'Source': 'WDEL', 'Bias': 'Center', 'Agree': 9, 'Disagree': 12} , 
    {'Source': 'WDIO', 'Bias': 'Center', 'Agree': 13, 'Disagree': 11} , 
    {'Source': 'WDIV 4', 'Bias': 'Center', 'Agree': 20, 'Disagree': 16} , 
    {'Source': 'WDIY', 'Bias': 'Center', 'Agree': 4, 'Disagree': 6} , 
    {'Source': 'WDSU', 'Bias': 'Center', 'Agree': 28, 'Disagree': 28} , 
    {'Source': 'WDTN 2', 'Bias': 'Center', 'Agree': 10, 'Disagree': 13} , 
    {'Source': 'WDTV 5', 'Bias': 'Center', 'Agree': 11, 'Disagree': 11} , 
    {'Source': 'Weatherford Democrat', 'Bias': 'Center', 'Agree': 8, 'Disagree': 6} , 
    {'Source': 'WEHT/WTVW', 'Bias': 'Center', 'Agree': 11, 'Disagree': 14} , 
    {'Source': 'WEMU', 'Bias': 'Center', 'Agree': 7, 'Disagree': 11} , 
    {'Source': 'WESH 2', 'Bias': 'Center', 'Agree': 18, 'Disagree': 18} , 
    {'Source': 'West Hawaii Today', 'Bias': 'Center', 'Agree': 24, 'Disagree': 24} , 
    {'Source': 'West Texas Tribune', 'Bias': 'Center', 'Agree': 13, 'Disagree': 8} , 
    {'Source': 'West Virginia Public Broadcasting', 'Bias': 'Center', 'Agree': 8, 'Disagree': 35} , 
    {'Source': 'Weston Democrat', 'Bias': 'Center', 'Agree': 9, 'Disagree': 10} , 
    {'Source': 'WFAE', 'Bias': 'Center', 'Agree': 232, 'Disagree': 255} , 
    {'Source': 'WFLA', 'Bias': 'Center', 'Agree': 12, 'Disagree': 14} , 
    {'Source': 'WFMZ 69', 'Bias': 'Center', 'Agree': 15, 'Disagree': 15} , 
    {'Source': 'WFSA', 'Bias': 'Lean Left', 'Agree': 16, 'Disagree': 21} , 
    {'Source': 'WFSB', 'Bias': 'Center', 'Agree': 14, 'Disagree': 13} , 
    {'Source': 'WFSU', 'Bias': 'Center', 'Agree': 9, 'Disagree': 11} , 
    {'Source': 'WFYI', 'Bias': 'Lean Left', 'Agree': 13, 'Disagree': 17} , 
    {'Source': 'WGAL 8', 'Bias': 'Center', 'Agree': 13, 'Disagree': 12} , 
    {'Source': 'WGBH', 'Bias': 'Center', 'Agree': 473, 'Disagree': 459} , 
    {'Source': 'WGME 13', 'Bias': 'Center', 'Agree': 7, 'Disagree': 8} , 
    {'Source': 'WGN', 'Bias': 'Center', 'Agree': 260, 'Disagree': 276} , 
    {'Source': 'WGVU', 'Bias': 'Center', 'Agree': 5, 'Disagree': 7} , 
    {'Source': 'Whatfinger News', 'Bias': 'Right', 'Agree': 286, 'Disagree': 230} , 
    {'Source': 'WHBC 1480', 'Bias': 'Center', 'Agree': 6, 'Disagree': 7} , 
    {'Source': 'WHDH 7', 'Bias': 'Center', 'Agree': 14, 'Disagree': 19} , 
    {'Source': 'WHIO 7', 'Bias': 'Center', 'Agree': 10, 'Disagree': 10} , 
    {'Source': 'Whitehouse.gov', 'Bias': 'Lean Left', 'Agree': 594, 'Disagree': 813} , 
    {'Source': 'Whittier Daily News', 'Bias': 'Center', 'Agree': 56, 'Disagree': 65} , 
    {'Source': 'WHNT 19', 'Bias': 'Center', 'Agree': 11, 'Disagree': 10} , 
    {'Source': 'WHO Radio 1040', 'Bias': 'Center', 'Agree': 10, 'Disagree': 12} , 
    {'Source': 'WHOP', 'Bias': 'Center', 'Agree': 5, 'Disagree': 8} , 
    {'Source': 'WHYY', 'Bias': 'Center', 'Agree': 25, 'Disagree': 15} , 
    {'Source': 'WIBW 13', 'Bias': 'Center', 'Agree': 11, 'Disagree': 16} , 
    {'Source': 'Wicked Local', 'Bias': 'Center', 'Agree': 9, 'Disagree': 8} , 
    {'Source': 'Will Reusch', 'Bias': 'Center', 'Agree': 10, 'Disagree': 10} , 
    {'Source': 'Willam A. Galston', 'Bias': 'Lean Left', 'Agree': 161, 'Disagree': 148} , 
    {'Source': 'William Barr', 'Bias': 'Lean Right', 'Agree': 20, 'Disagree': 26} , 
    {'Source': 'William Bennett', 'Bias': 'Right', 'Agree': 194, 'Disagree': 263} , 
    {'Source': 'William McGurn', 'Bias': 'Right', 'Agree': 146, 'Disagree': 102} , 
    {'Source': 'Williamson Herald', 'Bias': 'Center', 'Agree': 6, 'Disagree': 9} , 
    {'Source': 'WILX 10', 'Bias': 'Center', 'Agree': 15, 'Disagree': 16} , 
    {'Source': 'Winona Daily', 'Bias': 'Center', 'Agree': 13, 'Disagree': 14} , 
    {'Source': 'Winona Times', 'Bias': 'Center', 'Agree': 9, 'Disagree': 8} , 
    {'Source': 'Wired', 'Bias': 'Center', 'Agree': 552, 'Disagree': 952} , 
    {'Source': 'WIS 10', 'Bias': 'Center', 'Agree': 13, 'Disagree': 14} , 
    {'Source': 'Wis Politics', 'Bias': 'Center', 'Agree': 15, 'Disagree': 15} , 
    {'Source': 'Wisconsin Examiner', 'Bias': 'Lean Left', 'Agree': 12, 'Disagree': 13} , 
    {'Source': 'Wisconsin Gazette', 'Bias': 'Lean Left', 'Agree': 283, 'Disagree': 264} , 
    {'Source': 'Wisconsin Law Journal', 'Bias': 'Center', 'Agree': 8, 'Disagree': 20} , 
    {'Source': 'Wisconsin Public Radio', 'Bias': 'Center', 'Agree': 9, 'Disagree': 41} , 
    {'Source': 'Wisconsin Rapids Tribune', 'Bias': 'Center', 'Agree': 12, 'Disagree': 12} , 
    {'Source': 'Wisconsin State Journal', 'Bias': 'Center', 'Agree': 22, 'Disagree': 18} , 
    {'Source': 'Wisconsin Watch', 'Bias': 'Lean Left', 'Agree': 12, 'Disagree': 13} , 
    {'Source': 'Wish TV', 'Bias': 'Center', 'Agree': 18, 'Disagree': 14} , 
    {'Source': 'WITN', 'Bias': 'Center', 'Agree': 8, 'Disagree': 8} , 
    {'Source': 'WIVB 4', 'Bias': 'Center', 'Agree': 14, 'Disagree': 13} , 
    {'Source': 'WIZM', 'Bias': 'Center', 'Agree': 10, 'Disagree': 13} , 
    {'Source': 'WJAR 10', 'Bias': 'Center', 'Agree': 11, 'Disagree': 11} , 
    {'Source': 'WJCT News', 'Bias': 'Center', 'Agree': 7, 'Disagree': 10} , 
    {'Source': 'WJHG', 'Bias': 'Center', 'Agree': 16, 'Disagree': 16} , 
    {'Source': 'WJON', 'Bias': 'Center', 'Agree': 12, 'Disagree': 15} , 
    {'Source': 'WJTV 12', 'Bias': 'Center', 'Agree': 10, 'Disagree': 9} , 
    {'Source': 'WKAR', 'Bias': 'Center', 'Agree': 12, 'Disagree': 12} , 
    {'Source': 'WKBN 27', 'Bias': 'Center', 'Agree': 14, 'Disagree': 12} , 
    {'Source': 'WKRC 12', 'Bias': 'Center', 'Agree': 18, 'Disagree': 16} , 
    {'Source': 'WKRN News 2', 'Bias': 'Center', 'Agree': 12, 'Disagree': 18} , 
    {'Source': 'WKTN', 'Bias': 'Center', 'Agree': 5, 'Disagree': 6} , 
    {'Source': 'WKTV 2', 'Bias': 'Center', 'Agree': 9, 'Disagree': 10} , 
    {'Source': 'WKYC 3', 'Bias': 'Center', 'Agree': 16, 'Disagree': 17} , 
    {'Source': 'WKYT', 'Bias': 'Center', 'Agree': 11, 'Disagree': 9} , 
    {'Source': 'WLBT 3', 'Bias': 'Center', 'Agree': 12, 'Disagree': 14} , 
    {'Source': 'WLNS', 'Bias': 'Center', 'Agree': 16, 'Disagree': 16} , 
    {'Source': 'WLOX 13', 'Bias': 'Center', 'Agree': 12, 'Disagree': 10} , 
    {'Source': 'WMAR 2', 'Bias': 'Center', 'Agree': 8, 'Disagree': 11} , 
    {'Source': 'WMNF', 'Bias': 'Lean Left', 'Agree': 7, 'Disagree': 8} , 
    {'Source': 'WMTW 8', 'Bias': 'Center', 'Agree': 8, 'Disagree': 10} , 
    {'Source': 'WND', 'Bias': 'Right', 'Agree': 931, 'Disagree': 385} , 
    {'Source': 'WNDU 16', 'Bias': 'Center', 'Agree': 12, 'Disagree': 11} , 
    {'Source': 'WNKY 40', 'Bias': 'Center', 'Agree': 10, 'Disagree': 8} , 
    {'Source': 'WNYC', 'Bias': 'Lean Left', 'Agree': 13, 'Disagree': 23} , 
    {'Source': 'WOAI 4', 'Bias': 'Center', 'Agree': 14, 'Disagree': 12} , 
    {'Source': 'WOIO 19', 'Bias': 'Center', 'Agree': 22, 'Disagree': 19} , 
    {'Source': 'WOOD 8', 'Bias': 'Center', 'Agree': 19, 'Disagree': 22} , 
    {'Source': 'World Magazine', 'Bias': 'Right', 'Agree': 37, 'Disagree': 55} , 
    {'Source': 'World Wildlife', 'Bias': 'Center', 'Agree': 57, 'Disagree': 60} , 
    {'Source': 'Worthy News', 'Bias': 'Center', 'Agree': 22, 'Disagree': 17} , 
    {'Source': 'WOWK 13', 'Bias': 'Center', 'Agree': 10, 'Disagree': 10} , 
    {'Source': 'WPKY', 'Bias': 'Center', 'Agree': 5, 'Disagree': 6} , 
    {'Source': 'WPRI 12', 'Bias': 'Center', 'Agree': 12, 'Disagree': 11} , 
    {'Source': 'WRAL', 'Bias': 'Center', 'Agree': 19, 'Disagree': 27} , 
    {'Source': 'Wrangell Sentinel', 'Bias': 'Center', 'Agree': 13, 'Disagree': 15} , 
    {'Source': 'WRBI Radio', 'Bias': 'Center', 'Agree': 11, 'Disagree': 9} , 
    {'Source': 'WRDE', 'Bias': 'Center', 'Agree': 15, 'Disagree': 16} , 
    {'Source': 'WRDW', 'Bias': 'Center', 'Agree': 8, 'Disagree': 12} , 
    {'Source': 'WRFA', 'Bias': 'Center', 'Agree': 4, 'Disagree': 6} , 
    {'Source': 'WRKF', 'Bias': 'Lean Left', 'Agree': 8, 'Disagree': 9} , 
    {'Source': 'WSAZ 3', 'Bias': 'Center', 'Agree': 11, 'Disagree': 14} , 
    {'Source': 'WSFA 12', 'Bias': 'Center', 'Agree': 7, 'Disagree': 10} , 
    {'Source': 'WTKR 3', 'Bias': 'Center', 'Agree': 12, 'Disagree': 12} , 
    {'Source': 'WTMJ 4 Milwaukee', 'Bias': 'Center', 'Agree': 18, 'Disagree': 23} , 
    {'Source': 'WTNH', 'Bias': 'Center', 'Agree': 18, 'Disagree': 17} , 
    {'Source': 'WTOL 11', 'Bias': 'Center', 'Agree': 6, 'Disagree': 6} , 
    {'Source': 'WTOP', 'Bias': 'Center', 'Agree': 20, 'Disagree': 21} , 
    {'Source': 'WTRF', 'Bias': 'Center', 'Agree': 4, 'Disagree': 4} , 
    {'Source': 'WTRF 7', 'Bias': 'Center', 'Agree': 5, 'Disagree': 5} , 
    {'Source': 'WTTW', 'Bias': 'Center', 'Agree': 11, 'Disagree': 12} , 
    {'Source': 'WTVB', 'Bias': 'Center', 'Agree': 7, 'Disagree': 8} , 
    {'Source': 'WTVR 6', 'Bias': 'Center', 'Agree': 13, 'Disagree': 14} , 
    {'Source': 'WV Metro News', 'Bias': 'Center', 'Agree': 15, 'Disagree': 17} , 
    {'Source': 'WV News', 'Bias': 'Center', 'Agree': 13, 'Disagree': 17} , 
    {'Source': 'WVEC 13', 'Bias': 'Center', 'Agree': 16, 'Disagree': 17} , 
    {'Source': 'WVNews.com', 'Bias': 'Center', 'Agree': 25, 'Disagree': 27} , 
    {'Source': 'WVNS 59', 'Bias': 'Center', 'Agree': 6, 'Disagree': 5} , 
    {'Source': 'WVPE', 'Bias': 'Lean Left', 'Agree': 8, 'Disagree': 9} , 
    {'Source': 'WWAY 3', 'Bias': 'Center', 'Agree': 13, 'Disagree': 13} , 
    {'Source': 'WXOW', 'Bias': 'Lean Left', 'Agree': 11, 'Disagree': 15} , 
    {'Source': 'WYO 4', 'Bias': 'Center', 'Agree': 9, 'Disagree': 6} , 
    {'Source': 'WyoFile', 'Bias': 'Lean Right', 'Agree': 33, 'Disagree': 47} , 
    {'Source': 'Wyoming News Now', 'Bias': 'Center', 'Agree': 9, 'Disagree': 13} , 
    {'Source': 'Wyoming Public Media', 'Bias': 'Lean Left', 'Agree': 26, 'Disagree': 53} , 
    {'Source': 'WYSO Public Radio', 'Bias': 'Center', 'Agree': 8, 'Disagree': 30} , 
    {'Source': 'WZFG The Flag', 'Bias': 'Center', 'Agree': 15, 'Disagree': 13} , 
    {'Source': 'Yahoo News', 'Bias': 'Lean Left', 'Agree': 5127, 'Disagree': 3583} , 
    {'Source': 'Yahoo! The 360', 'Bias': 'Mixed', 'Agree': 259, 'Disagree': 447} , 
    {'Source': 'Yakima Herald-Republic', 'Bias': 'Center', 'Agree': 17, 'Disagree': 22} , 
    {'Source': 'Yash Goenka', 'Bias': 'Lean Left', 'Agree': 13, 'Disagree': 23} , 
    {'Source': 'Yasmin Tavakoli', 'Bias': 'Center', 'Agree': 55, 'Disagree': 63} , 
    {'Source': 'Yes! Magazine', 'Bias': 'Left', 'Agree': 507, 'Disagree': 285} , 
    {'Source': 'York Dispatch', 'Bias': 'Center', 'Agree': 15, 'Disagree': 15} , 
    {'Source': 'Your Sun', 'Bias': 'Center', 'Agree': 10, 'Disagree': 11} , 
    {'Source': 'Yuma Sun', 'Bias': 'Center', 'Agree': 14, 'Disagree': 11} , 
    {'Source': 'Zachary Dickstein', 'Bias': 'Left', 'Agree': 7, 'Disagree': 4} , 
    {'Source': 'Zack Beauchamp', 'Bias': 'Lean Left', 'Agree': 45, 'Disagree': 52} , 
    {'Source': 'Zeeshan Aleem', 'Bias': 'Left', 'Agree': 53, 'Disagree': 35} , 
    {'Source': 'ZeroHedge', 'Bias': 'Lean Right', 'Agree': 304, 'Disagree': 246}
]

# News hardcodes
newsHardcodes = {
    "Yahoo Finance" : "Yahoo News"
}

## Get Google News data
## Input: query
## Output: raw google news data
def getGoogleNewsData(query, period):
    # Query from Google News page
    gn_query = GoogleNews()
    gn_query = GoogleNews(lang='en', region='US')
    gn_query = GoogleNews(encode='utf-8')
    gn_query = GoogleNews(period='7d')
    gn_query.get_news(query)
    newsdf = gn_query.results()

    # Query from Google Search news section page
    gs_query = GoogleNews()
    gs_query = GoogleNews(lang='en', region='US')
    gs_query = GoogleNews(encode='utf-8')
    gs_query = GoogleNews(period=period)
    gs_query.search(query)
    searchdf = gs_query.results()

    return newsdf + searchdf

## Get articles
## Input: google news data
## Output: reputed articles, unreputed articles
def getArticles(googleNewsData):
    unreputed = []
    reputed = []

    for article in googleNewsData:
        title = article['title']
        media = article['media']
        r_timestamp = article['date']
        timestamp = article['datetime']
        link = article['link']

        # Convert timestamp to string
        timestamp = str(timestamp)
        
        # Validate titles
        title = title.replace(media+"More", "")

        # Validate links
        if(link[:4] != "http"):
            link = "https://" + link

        # Hardcode popular newsources
        if(media in newsHardcodes):
            media = newsHardcodes[media]
        
        # Get source info from mbdf data        
        def find(lst, value):
            for i, dic in enumerate(lst):
                if dic['Source'] == value:
                    return i
            return -1
        
        src_index = find(mbdf2, media)

        # Unreputed source
        if(src_index == -1):
            unreputed.append({
                "title": title,
                "media" : media,
                "r_timestamp" : r_timestamp,
                "timestamp" : timestamp,
                "link" : link,
                # "article_text" : article_text,
                # "article_summary" : article_summary
            })
        # Reputed source
        else:
            # src_name = src_info["Source"].values[0]
            src_name = mbdf2[src_index]["Source"]
            # src_bias = src_info["Bias"].values[0]
            src_bias = mbdf2[src_index]["Bias"]
            # src_agree = int(src_info["Agree"].values[0])
            src_agree = int(mbdf2[src_index]["Agree"])
            # src_disagree = int(src_info["Disagree"].values[0])
            src_disagree = int(mbdf2[src_index]["Disagree"])

            reputed.append({
                "title": title,
                "media" : media,
                "r_timestamp" : r_timestamp,
                "timestamp" : timestamp,
                "link" : link,
                # "article_text" : article_text,
                # "article_summary" : article_summary,
                "src_name" : src_name,
                "src_bias" : src_bias,
                "src_agree" : src_agree,
                "src_disagree" : src_disagree,
            })
    return {
        "unreputed" : unreputed,
        "reputed" : reputed
    }


## Rank reputed articles
## Input: reputed articles
## Output: parsed ranked reputed articles [5], unranked reputed articles
def rankReputedArticles(query, reputedArticles):
    # Create prompt
    prompt = "Which article is the most reliable and most relevant to " + query + "? (based on seriousness of title, when it was published, political bias, and the number of people agreeing with the source compared to the number disagreeing)"
    docs = []

    for article in reputedArticles:
        title = article['title']
        r_timestamp = article['r_timestamp']
        source_bias = article['src_bias']
        source_agree = article['src_agree']
        source_disagree = article['src_disagree']

        doc = "title: " + title + ", time published: " + r_timestamp + ", source political bias: " + source_bias + ", people agreeing with source: " + str(source_agree) + ", people disagreeing with source: " + str(source_disagree)
        
        docs.append(doc)
    
    # Execute prompt
    n_articles = len(reputedArticles)
    results = co.rerank(query=prompt, documents=docs, top_n=n_articles, model='rerank-english-v2.0') # Change top_n to change the number of results returned. If top_n is not passed, all results will be returned.
    # Parse output
    parsed_results = []

    i_rank = 1

    for result in results:
        i = result["index"]
        relevance_score = result["relevance_score"]

        parsed_results.append({
            "rank" : i_rank,
            "index" : i,
            "relevance_score" : relevance_score
        })

        i_rank += 1


    return parsed_results

## Rank unreputed articles
## Input: unreputed articles
## Output: parsed ranked unreputed articles [5], unranked unreputed articles
def rankUnreputedArticles(query, unreputedArticles):
    # Create prompt
    prompt = "Which article seems the most legitimate and relevant to " + query + " (based on seriousness of title and when it was published)?"
    docs = []

    for article in unreputedArticles:
        title = article['title']
        r_timestamp = article['r_timestamp']

        doc = "title: " + title + ", published: " + r_timestamp

        docs.append(doc)
    
    # Execute prompt
    n_articles = len(unreputedArticles)
    results = co.rerank(query=prompt, documents=docs, top_n=n_articles, model='rerank-english-v2.0') # Change top_n to change the number of results returned. If top_n is not passed, all results will be returned.
    
    # Parse output
    parsed_results = []

    resultObj = None
    for result in results:
        result = tuple(result)
        if(result[0] == 'results'):
            resultObj = result[1]

    for idx, r in enumerate(resultObj):
        r = r.dict()
        i = r["index"]
        relevance_score = r["relevance_score"]
        rank = idx + 1

        parsed_results.append({
            "rank" : rank,
            "index" : i,
            "relevance_score" : relevance_score
        })

    return parsed_results


## Summarize article
## Input: raw article
## Output: summarized article
def summarizeArticle(article):
    response = co.summarize(
            text=article,
            format="bullets",
            model='command',
            length='medium',
            extractiveness='medium'
        )
    return response.summary

## Parse article
## Input: link
## Output: parsed data or null
def parseArticle(link):
    # Get article from link
    try:
        article = Article(link)
        article.download()
        article.parse()
        article_text = article.text

        # Don't allow articles that are less than 250 characters (for API purposes)
        if(len(article_text) < 250):
            return {}

        # Get article summary
        return {
            "text" : article_text,
            "summary" : summarizeArticle(article=article_text)
        }
    except:
        return {}

## Parse articles
## Input: ranked reputed / unreputed articles
## Output: parsed ranked reputed / unreputed articles, unparsed ranked reputed / unreputed articles
def parseArticles(data, n_articles, ranks): 
    parsed = []
    unparsed = []

    finishedParsing = False
    for article_rank in ranks:
        # Get ranks
        # Article index
        i = article_rank["index"]
        # Article rank (overall)
        rank = article_rank["rank"]
        # Article relevance score
        relevance_score = article_rank["relevance_score"]
        
        # Article data
        article = data[i]
        
        article["rank"] = rank
        article["relevance_score"] = relevance_score

        # If finished parsing, add article to unparsed articles
        if(finishedParsing == True):
            unparsed.append(article)
            continue

        # Attempt to parse article
        p_article = parseArticle(article["link"])

        # Article is parsed
        if(len(p_article) != 0):
            article["text"] = p_article["text"]
            article["summary"] = p_article["summary"]
            parsed.append(article)
        # Article is unparsed
        else:
            unparsed.append(article)

        if(len(parsed) == n_articles):
            finishedParsing = True
        
    return {
        "parsed" : parsed,
        "unparsed" : unparsed
    }

## Get reputed articles consensus
## Input: parsed ranked reputed articles [5]
## Output: reputed article consensus
def getReputedArticlesConsensus(parsedRankedReputedArticles):
    prompt = ""
    additional_prompt = "Given the following articles, develop a general consensus based on each article's title and summary grouping by timestamp (how recent it was published)"

    for article in parsedRankedReputedArticles:
        title = article["title"]
        summary = article["summary"]
        timestamp = article["r_timestamp"]
        prompt += "Article Title: " + title + "\n"
        prompt += "Article Timestamp: " + timestamp + "\n"
        prompt += "Article Summary: " + summary + "\n\n"
    
    response = co.summarize(
        text=prompt,
        format="bullets",
        extractiveness="high",
        temperature=0.7,
        additional_command=additional_prompt
    )

    return response.summary

## Get unreputed articles consensus
## Input: parsed ranked unreputed articles [5]
## Output: unreputed article consensus
def getUnreputedArticlesConsensus(parsedRankedUnreputedArticles):
    prompt = ""
    additional_prompt = "Given the following articles, develop a general consensus based on each article's title and summary grouping by timestamp (how recent it was published)"

    for article in parsedRankedUnreputedArticles:
        title = article["title"]
        summary = article["summary"]
        timestamp = article["r_timestamp"]
        prompt += "Article Title: " + title + "\n"
        prompt += "Article Timestamp: " + timestamp + "\n"
        prompt += "Article Summary: " + summary + "\n\n"
    
    response = co.summarize(
        text=prompt,
        format="bullets",
        extractiveness="high",
        temperature=0.7,
        additional_command=additional_prompt
    )

    return response.summary

# Get overall articles consensus
# Input: reputed article consensus, unreputed article consensus
# Output: overall consensus
def getOverallConsensus(query, reputedArticlesConsensus, unreputedArticlesConsensus):
    prompt = ""
    additional_prompt = "Given the consensus formed from reputed articles and the consensus formed from unreputed articles, develop an overall, holistic consensus on the future outlook of " + query

    prompt += "Reputed articles consensus: " + reputedArticlesConsensus + "\n"
    prompt += "Unreputed articles consensus: " + unreputedArticlesConsensus
    
    response = co.summarize(
        text=prompt,
        format="bullets",
        extractiveness="high",
        temperature=0.7,
        additional_command=additional_prompt
    )

    return response.summary


def buildJson2(query, period, rdepth, udepth):
    googleNewsData = getGoogleNewsData(query, period=period)

    articles = getArticles(googleNewsData=googleNewsData)
    reputedArticles = articles["reputed"]
    unreputedArticles = articles["unreputed"]

    reputedRanks = rankReputedArticles(query=query, reputedArticles=reputedArticles)
    unreputedRanks = rankUnreputedArticles(query=query, unreputedArticles=unreputedArticles)

    parsedReputedArticles = parseArticles(data=reputedArticles, n_articles=int(rdepth), ranks=reputedRanks)
    parsedReputed = parsedReputedArticles["parsed"]
    unparsedReputed = parsedReputedArticles["unparsed"]

    parsedUnreputedArticles = parseArticles(data=unreputedArticles, n_articles=int(udepth), ranks=unreputedRanks)
    parsedUnreputed = parsedUnreputedArticles["parsed"]
    unparsedUnreputed = parsedUnreputedArticles["unparsed"]

    reputedArticleConsensus = getReputedArticlesConsensus(parsedRankedReputedArticles=parsedReputed)
    unreputedArticleConsensus = getUnreputedArticlesConsensus(parsedRankedUnreputedArticles=parsedUnreputed)

    overallConsensus = getOverallConsensus(query=query, reputedArticlesConsensus=reputedArticleConsensus, unreputedArticlesConsensus=unreputedArticleConsensus)

    return {
        "parsedReputed" : parsedReputed,
        "unparsedReputed" : unparsedReputed,
        "reputedArticleConsensus" : reputedArticleConsensus,

        "parsedUnreputed" : parsedUnreputed,
        "unparsedUnreputed" : unparsedUnreputed,
        "unreputedArticleConsensus" : unreputedArticleConsensus,

        "overallConsensus" : overallConsensus
    }
