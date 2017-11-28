import newspaper
from newspaper import news_pool

conservation_terms = []
sources = newspaper.popular_urls()
built_papers = []


def build_papers():
    for paper_url in sources():
        paper = newspaper.build(paper_url)
        built_papers.append(paper)


def create_pool():
    news_pool.set(built_papers, threads_per_source=1)
    news_pool.join()