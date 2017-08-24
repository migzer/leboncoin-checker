import urllib2
import sys
import smtplib

from email.mime.text import MIMEText
from geopy.geocoders import Nominatim

def get_cleanCategory(category):
    i = 0;
    new_category = "";
    while (i < len(category)):
        if (str(category[i].isalpha()) == "True"):
            new_category += category[i];
        elif (i != len(category)):
            new_category += "_";
            while (str(category[i + 1].isalpha()) != "True" and i + 1 < len(category)):
                i += 1;
        i += 1;
    return (new_category);

def get_url(category, location, radius, rental):
    url = ("https://www.leboncoin.fr/" + category + "/" + "?w=4" + "&latitude="
    + str(location.latitude) + "&longitude=" + str(location.longitude) + "&radius=" + str(radius)
           + "&mre=" + str(rental[0]) + "&mrs=" + str(rental[1]));
    return (url);

def get_location():
    print("What adress do you want to search for ?");
    position = raw_input();
    geolocator = Nominatim();
    location = geolocator.geocode(position);
    return (location);

def get_radius():
    radius = -1;
    while (radius != 10 and radius != 20 and radius != 30 and radius != 50 and
           radius != 100 and radius != 200):
        print("Within radius of 10, 20, 30, 50, 100 or 200 km ?");
        radius = int(raw_input());
    return (radius * 1000);

def get_category():
    category = "";
    print("What category do you want to search for ?");
    category = raw_input();
    category = category.lower();
    category = get_cleanCategory(category);
    return (category);

def get_rental():
    rental = [];
    print("Rent up to ?");
    mre = int(raw_input());
    rental.append(mre);
    print("Rent minimum ?");
    mrs = int(raw_input());
    rental.append(mrs);
    return (rental);

def get_sourcePage(url):
    request = urllib2.Request(url);
    handle = urllib2.urlopen(request);
    source_page = handle.read();
    return (source_page);

def get_mailSendTo():
    mail = "";
    while ("@" not in mail):
        print("To wich mail to send an alert ?");
        mail = raw_input();
    return (mail);

def parse_sourcePage(source_page):
    i = 1;
    title = [];
    source_page = source_page.split("<li itemscope");
    while (i < len(source_page)):
        title.append(source_page[i].split("class=")[0].split("title=")[1]);
        i += 1;
    return (title);

def send_mail(new_announce, mail, mail_content):
    botMail = "miguel1601@hotmail.fr";
    msg = MIMEText(mail_content, "html");
    msg["Subject"] = new_announce;
    msg["From"] = botMail;
    msg["To"] = mail;

    s = smtplib.SMTP("smtp.live.com", 587);
    s.ehlo();
    s.starttls();
    s.ehlo();
    s.login(botMail, "Caligada35");
    s.sendmail(botMail, mail, msg.as_string());
    s.quit();

def get_titleLink(keyword, source_page):
    title_link = source_page.split(keyword)[0];
    title_link = title_link.split("href");
    title_link = title_link[len(title_link) - 1];
    title_link = title_link.split(" ")[0];
    title_link = title_link[2:];
    title_link = title_link[:-1];
    return ("http:" + title_link);

def main():
    title = [];
    location = get_location();
    radius = get_radius();
    category = get_category();
    if (str(category) == "locations"):
        rental = get_rental();
    url = get_url(category, location, radius, rental);
    mail = get_mailSendTo();
    source_page = get_sourcePage(url);
    title = parse_sourcePage(source_page);
    title_link = get_titleLink(title[0], source_page);
    mail_content = get_sourcePage(title_link);
    send_mail(title[0], mail, mail_content);

if __name__ == "__main__":
    main();
