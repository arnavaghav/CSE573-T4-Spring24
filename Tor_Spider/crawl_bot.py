from get_domains import *
from file_manage import *
from link_finder import link_crawler
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import tldextract


#Importing Stem libraries
from stem import Signal
from stem.control import Controller
import socks, socket

#Initiating Connection
with Controller.from_port(port=9051) as controller:
    controller.authenticate("alphabets")
    controller.signal(Signal.NEWNYM)

# TOR SETUP GLOBAL Vars
SOCKS_PORT = 9050  # TOR proxy port that is default from torrc, change to whatever torrc is configured to
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", SOCKS_PORT)
socket.socket = socks.socksocket

# Perform DNS resolution through the socket
def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo


class Crawl_bot:

    folder_name, start_link, domain_name, queued_data, crawled_data = '', '', '', '', ''
    queue = set()
    data_crawled = set()

    def __init__(self, folder_name, start_link, domain_name):
        Crawl_bot.folder_name = folder_name
        Crawl_bot.start_link = start_link
        Crawl_bot.domain_name = domain_name
        Crawl_bot.queued_data = Crawl_bot.folder_name + '/queue.txt'
        Crawl_bot.crawled_data = Crawl_bot.folder_name + '/crawled.txt'
        Crawl_bot.count = 0
        self.initiate_directory()
        self.crawl_page('Spider starts here', Crawl_bot.start_link)

    @staticmethod
    def initiate_directory():                   # Define and create new directory on the first run
        create_project_folder(Crawl_bot.folder_name)
        create_data_files(Crawl_bot.folder_name, Crawl_bot.start_link)
        Crawl_bot.queue = convert_to_set(Crawl_bot.queued_data)
        Crawl_bot.data_crawled = convert_to_set(Crawl_bot.crawled_data)

    @staticmethod
    def crawl_page(thread_name, web_url):      # Fill queue and then update files, also updating user display
        #print(web_url)
        if web_url not in Crawl_bot.data_crawled:
            # print(f"{thread_name}: {Crawl_bot.count}")
            if Crawl_bot.count % 500 == 0:
              print(thread_name + ' now crawl starts ' + web_url)
              print('Queue_url ' + str(len(Crawl_bot.queue)) + ' | Crawled_url  ' + str(len(Crawl_bot.data_crawled)))

            try:
              Crawl_bot.count += 1
              Crawl_bot.add_url_to_queue(Crawl_bot.collect_url(web_url))
              Crawl_bot.queue.remove(web_url)
              Crawl_bot.data_crawled.add(web_url)
              Crawl_bot.update_folder()
            except Exception as e:
                print(str(e))

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def collect_url(web_url):
        html_data_string = ''
        try:
            received_response = urlopen(web_url, timeout=10)
            if 'text/html' in received_response.getheader('Content-Type'):
                data_bytes = received_response.read()
                html_data_string = data_bytes.decode("latin-1")
            link_finder = link_crawler(Crawl_bot.start_link, web_url)
            link_finder.feed(html_data_string)

##############################################################################################################################################################################################
#######################################FOR SCRAPPING PURPOSES#################################################################################################################################
            f = open(Crawl_bot.folder_name + '/' + ((tldextract.extract(web_url)).domain), 'w')
            f.write(html_data_string)
            f.close()
###############################################################################################################################################################################################
###############################################################################################################################################################################################

        except HTTPError as error:
            #print(f"Data not retrieved because {error}")
            return set()
        except URLError as error:
            #if isinstance(error.reason, socket.timeout):
                #print(f"Socket timed out")
            #else:
                #print(f"Misc error {error}")
            return set()
        except Exception as e:
            #print(str(e))
            return set()
        return link_finder.page_urls()


    @staticmethod
    def add_url_to_queue(links):          # Queue data saves to project files
        for url in links:
            if (url in Crawl_bot.queue) or (url in Crawl_bot.data_crawled):
                continue
            Crawl_bot.queue.add(url)


    @staticmethod
    def update_folder():                    # Update the project directory
        set_to_file(Crawl_bot.queue, Crawl_bot.queued_data)
        set_to_file(Crawl_bot.data_crawled, Crawl_bot.crawled_data)