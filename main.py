import requests
import getpass
import cgi
import os
import sys
import bs4

post_data = {
    'username': 'YOUR_USERNAME_HERE',
    'password': 'YOUR_PASSWORD_HERE'
}

enable_file_type = ['document', 'powerpoint', 'spreadsheet', 'pdf', 'archive']
dir_path = os.path.dirname(os.path.realpath(__file__))


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def get_course_list(session, url):
    if post_data['username'] is 'YOUR_USERNAME_HERE' and post_data['password'] is 'YOUR_PASSWORD_HERE':
        print("Default ID & Password not found.")
        post_data['username'] = str(input('Your iSpace username:'))
        post_data['password'] = str(getpass.getpass(prompt='Your iSpace password: ', stream=None))
    moodle = session.post(url, post_data)
    homepage = bs4.BeautifulSoup(moodle.text, 'html.parser')

    courses = homepage.find_all('p', class_='tree_item branch')
    course_list = []
    for course in courses:
        if course.find_all('a'):
            for course_info in course.find_all('a'):
                course_list.append({'title': course_info.text,
                                    'url': course_info.get('href')})
    return course_list


def print_course_list(course_list):
    print("{:<5} {:<60} {:<55}".format('#', 'Course Title', 'URL'))
    for item in range(len(course_list)):
        print("{:<5} {:<60} {:<55}".format(item + 1,
                                           course_list[item]['title'],
                                           course_list[item]['url']))


def get_course_resources(session, url):
    course = session.get(url)
    course_page = bs4.BeautifulSoup(course.text, 'html.parser')
    course_title = course_page.find('title').text[8:]
    print('Fetching Course: {:}'.format(course_title))
    resources = course_page.find_all('div', class_='activityinstance')
    resources_summary = {}
    resources_list = []
    file_counter = 0
    for resource in resources:
        resource_info = {'title': resource.text,
                         'url': resource.find('a').get('href'),
                         'type': resource.find('img').get('src').split('/')[-1].split('-')[0]
                         }
        if resource_info['type'] in enable_file_type:
            if resource_info['type'] not in resources_summary:
                resources_summary[resource_info['type']] = 0
            resources_summary[resource_info['type']] += 1
            file_counter += 1
            resources_list.append(resource_info)
    print("---------------------------")
    print("Found {:} files:".format(file_counter))
    for file_type in resources_summary.keys():
        print("{:<15} | {:<3}".format(file_type, resources_summary[file_type]))
    respond = {"course_title": course_title,
               "resources_list": resources_list}
    return respond


def downloader(session, url, path):
    file1 = session.get(url)
    file = open(os.path.join(path, cgi.parse_header(file1.headers['Content-Disposition'])[-1]['filename']), 'wb')
    file.write(file1.content)
    print('Downloaded: ' + cgi.parse_header(file1.headers['Content-Disposition'])[-1]['filename'])
    file.close()


if __name__ == '__main__':
    requests_session = requests.Session()
    moodle_url = 'https://ispace.uic.edu.hk/login/index.php'
    my_course_list = get_course_list(requests_session, moodle_url)
    print_course_list(my_course_list)
    download_course = int(input("Which course do you want to download (integer index number): "))
    my_course_resources = get_course_resources(requests_session, my_course_list[download_course - 1]['url'])
    my_resources_list = my_course_resources["resources_list"]
    if query_yes_no("Do you want to download this files?"):
        file_dir = os.path.join(dir_path, 'download')
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_dir = os.path.join(file_dir, my_course_resources["course_title"])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        print("Files will download to: " + file_dir)
        for item in my_resources_list:
            downloader(requests_session, item['url'], file_dir)
        print("Finished.")
