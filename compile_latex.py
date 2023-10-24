import ads as ads
from copy import copy

class publicationHandler():
    def __init__(self,firstname,lastname,get_all_attributes=False):
        if(get_all_attributes):
            attributes = ['abstract','build_citation_tree','first_author_norm','keys','pubdate',
                        'aff','build_reference_tree','id','keyword','read_count',
                        'author','citation','identifier','metrics','reference',
                        'bibcode','citation_count','issue','page','title',
                        'bibstem','database','items','property','volume',
                        'bibtex','first_author','iteritems','pub','year']
        else:
            attributes = ['author','bibcode','title','first_author','pub','year']
        self.papers = list(ads.SearchQuery(author=f"{lastname}, {firstname}",
            fl=attributes))
        self.firstname = firstname
        self.lastname = lastname
        print(f"Found {len(self.papers)} papers for {firstname} {lastname}")

    def get_paper_info(self,paper,author):
        refereed = not ('arxiv' in paper.pub.lower())
        firstauthor = author in paper.first_author
        is_code = (paper.pub == 'Astrophysics Source Code Library')
        return refereed,firstauthor,is_code

    def write_author(self,authorstr,author):
        try:
            lastname, firstname = authorstr.split(", ")
            if author in authorstr:
                return f"\\textbf{{{firstname[0]}.~{lastname}}}"
            else:
                return f"{firstname[0]}.~{lastname}"
        except Exception as e:
            import warnings
            warnings.warn(f"Author '{authorstr}' has no first name")
            return authorstr

    def replace_dict_in_string(self,text, dic):
        text = copy(text)
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    def print_latex_paper_info_from_string(self,paper,author,max_authors,cvstr=None):
        if cvstr is None:
            cvstr = r"\cventry{JOURNAL}{TITLE}{}{YEAR}{}{AUTHORS}"
        journal = paper.pub
        reference_link = f"https://ui.adsabs.harvard.edu/abs/{paper.bibcode}/abstract"
        title = paper.title[0]
        title = f"\\href{{{reference_link}}}{{{title}}}"
        year = paper.year
        authors = ""
        author_count = 0
        contains_author = False
        # if len(paper.author) > max_authors:
        #     authors = self.write_author(paper.author[0],author) + " et al."
        #     if not author in paper.author[0]:
        #         authors += f" (incl. \\textbf{{{self.firstname[0]}.~{self.lastname}}})"

        for a in paper.author:
            if author_count < max_authors:
                authors += self.write_author(a,author)
                if author in a:
                    contains_author = True
                author_count += 1
                if(a != paper.author[-1]):
                    authors += ", "
            else:
                authors += " et al."
                if not contains_author:
                    authors += f" (incl. \\textbf{{{self.firstname[0]}.~{self.lastname}}})"
                break

        
        return self.replace_dict_in_string(cvstr,{'JOURNAL':journal,'TITLE':title,'YEAR':year,'AUTHORS':authors,'REFERENCE_LINK':reference_link})



    def print_first_author_publications(self,fstream,cvstr,max_authors):
        for paper in self.papers:
            refereed,firstauthor,is_code = self.get_paper_info(paper,self.lastname)
            if firstauthor and refereed and not is_code:
                fstream.write(self.print_latex_paper_info_from_string(paper,self.lastname,max_authors,cvstr))
                fstream.write("\n")

    def print_coauthor_publications(self,fstream,cvstr,max_authors):
        for paper in self.papers:
            refereed,firstauthor,is_code = self.get_paper_info(paper,self.lastname)
            if not firstauthor and refereed and not is_code:
                fstream.write(self.print_latex_paper_info_from_string(paper,self.lastname,max_authors,cvstr))
                fstream.write("\n")

    def print_code_publications(self,fstream,cvstr,max_authors):
        for paper in self.papers:
            refereed,firstauthor,is_code = self.get_paper_info(paper,self.lastname)
            if refereed and is_code:
                fstream.write(self.print_latex_paper_info_from_string(paper,self.lastname,max_authors,cvstr))
                fstream.write("\n")

    def print_preprints(self,fstream,cvstr,max_authors):
        for paper in self.papers:
            refereed,firstauthor,is_code = self.get_paper_info(paper,self.lastname)
            if not refereed:
                fstream.write(self.print_latex_paper_info_from_string(paper,self.lastname,max_authors,cvstr))
                fstream.write("\n")

    def print_first_author_preprints(self,fstream,cvstr,max_authors):
        for paper in self.papers:
            refereed,firstauthor,is_code = self.get_paper_info(paper,self.lastname)
            if firstauthor and not refereed:
                fstream.write(self.print_latex_paper_info_from_string(paper,self.lastname,max_authors,cvstr))
                fstream.write("\n")

    def print_coauthor_preprints(self,fstream,cvstr,max_authors):
        for paper in self.papers:
            refereed,firstauthor,is_code = self.get_paper_info(paper,self.lastname)
            if not firstauthor and not refereed:
                fstream.write(self.print_latex_paper_info_from_string(paper,self.lastname,max_authors,cvstr))
                fstream.write("\n")

    def make_publication_list_latex(self,fstr,cvstr=None,max_authors=5):
        with open(fstr,"w") as fstream:
            fstream.write("\\section{Publications}\n")
            fstream.write("\\subsection{First-author Publications}\n")
            self.print_first_author_publications(fstream,cvstr,max_authors)
            fstream.write("\\subsection{Co-authored Publications}\n")
            self.print_coauthor_publications(fstream,cvstr,max_authors)
            fstream.write("\\subsection{Code Publications}\n")
            self.print_code_publications(fstream,cvstr,max_authors)
            fstream.write("\\subsection{Preprints}\n")
            self.print_first_author_preprints(fstream,cvstr,max_authors)
            self.print_coauthor_preprints(fstream,cvstr,max_authors)

if __name__ == "__main__":
    import configparser
    import sys
    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    firstname = config['DEFAULT']['firstname']
    lastname = config['DEFAULT']['lastname']
    cvstr = config.get('DEFAULT','output_string',fallback=None)
    output_file = config['DEFAULT']['output_file']
    max_authors = int(config.get('DEFAULT','max_authors',fallback=5))
    ph = publicationHandler(firstname,lastname)
    ph.make_publication_list_latex(output_file,cvstr,max_authors)