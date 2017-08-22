import urllib2
import sys

def get_url(keywords):
    keywords = keywords.split();
    i = 0;
    url = "https://www.youtube.com/results?q=";
    while i <= len(keywords) - 1:
        url += keywords[i];
        i += 1;
        if i != len(keywords):
            url += "+";
    return url;

def main(keywords):
    url = get_url(keywords);
    print("URL: " + url);

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missed search !");
    else:
        main(sys.argv[1]);
