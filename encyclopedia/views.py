from django.shortcuts import render
from . import util
import markdown2
from django.shortcuts import redirect

from markdown2 import Markdown

error= {"message": "ERROR: This entry does not exist" }
entries = util.list_entries()






#converts markdown content to html
def md_to_html(title):
    content= util.get_entry(title)
    markdowner = markdown2.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)




#INDEX: Updates index.html such that, instead of merely listing the names of all pages in the encyclopedia,
#user can click on any entry name to be taken directly to that entry page.
def index(request):
    # file = {"entries": entries}
    file = util.list_entries()
    return render(request, "encyclopedia/index.html", { "entries": file} )




# ENTRY: Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry,
#should render a page that displays the contents of that encyclopedia entry.
#The view should get the content of the encyclopedia entry by calling the appropriate util function.
#If an entry is requested that does not exist,
#the user should be presented with an error page indicating that their requested page was not found.
#If the entry does exist, the user should be presented with a page that displays the content of the entry.
#The title of the page should include the name of the entry.
def entry(request, title):
    content= md_to_html(title)
    file= {"title": title , "content": content }
    if content == None:
        return render(request, "encyclopedia/error.html", error)
    else:
        return render(request, "encyclopedia/entry.html", file)







#SEARCH: Allows the user to type a query into the search box in the sidebar to search for an encyclopedia entry.
#If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
#If the query does not match the name of an encyclopedia entry, the user should instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring.
#For example, if the search query were ytho, then Python should appear in the search results.
#Clicking on any of the entry names on the search results page should take the user to that entry’s page.
def search(request):
    searchquery= request.POST['q']
    content= md_to_html(searchquery)
    file= {"title": searchquery , "content": content }
    matches= []

    if util.get_entry(searchquery):
        return render(request, "encyclopedia/entry.html", file )

    else:
        for entry in entries:
            if searchquery.lower() in entry.lower():
                matches.append(entry)
            did_you_mean = {"did_you_mean": matches}
        return render(request, "encyclopedia/search.html", did_you_mean)

        if not empty_list:
            return render(request, "encyclopedia/search.html", error)







# Clicking “Create New Page” in the sidebar should take the user to a page where they can create a new encyclopedia entry.
#Users should be able to enter a title for the page and, in a textarea, should be able to enter the Markdown content for the page.
#Users should be able to click a button to save their new page.
#When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
#Otherwise, the encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s page.
def new_page(request):

    error= {"message": "Entry page exists. Try something different"}

    if request.method == "GET":
        return render (request, "encyclopedia/new_page.html")

    elif request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        title_exists = util.get_entry(title)
        if title_exists == None:
            
            util.save_entry(title,  bytes(content, 'utf8'))
            return redirect('entry', title=title)
        else:
            return render(request, "encyclopedia/error.html" , error)








#On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.
#The textarea should be pre-populated with the existing Markdown content of the page. (i.e., the existing content should be the initial value of the textarea).
#The user should be able to click a button to save the changes made to the entry.
#Once the entry is saved, the user should be redirected back to that entry’s page.



#Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.
