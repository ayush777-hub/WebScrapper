from FileInputProcessor import FileInputProcessor
from Models.FileInput import FileInput
from PageAnalyzer import PageAnalyzer
from SearchAggregator import SearchAggregator
from SearchEngines.GoogleSearchEngine import GoogleSearchEngine
from SiteScrapper import SiteScrapper

if __name__ == '__main__':
    googleEngine = GoogleSearchEngine()
    searchAggregator = SearchAggregator([googleEngine])

    fileInput = FileInput("inputQuery.txt")
    inputProcessor = FileInputProcessor()
    queries = inputProcessor.ProcessInput(fileInput)

    for query in queries:
        sites_to_scrape = searchAggregator.GetSitesToScrape(query)
        for site in sites_to_scrape:
            if(site.__contains__('.pdf')): continue  # Skip PDF links
            if(site.__contains__('.jpg')): continue  # Skip image links
            if(site.__contains__('.png')): continue
            if(site.__contains__('.gif')): continue
            if(site.__contains__('.mp4')): continue
            
            scrapper = SiteScrapper(site)
            content = scrapper.fetch_content()
            if content: 
                analyzer = PageAnalyzer()
                productDetails = analyzer.analyze(content, query)
                print("Product details for site '{}': {}".format(site, productDetails))