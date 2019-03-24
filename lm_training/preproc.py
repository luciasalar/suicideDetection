import csv
import nltk
from sys import argv

def get_training_set_worker(filename: str, outfile: str) -> None:
    infile = open(filename, 'r')
    outfile = open(outfile, 'w')
    csvfile = csv.reader(infile)
    row0 = True
    for row in csvfile:
        if row0:
            row0 = False
            continue
        title = row[2].replace(".", " . ").replace("!", " ! ").replace("?", " ? ")
        txt = nltk.sent_tokenize(row[1].replace(".", " . ").replace("!", " ! ").replace("?", " ? "))
        tokeep = []
        for sent in txt:
            if len(sent.split()) > 3:
                tokeep.append(sent)
        outfile.write(title + '\n' + "\n".join(tokeep) + "\n")
    infile.close()
    outfile.close()

def get_test_set_worker(filename: str, outfolder: str, outclass: str) -> None:
    infile = open(filename, 'r')
    csvfile = csv.reader(infile)
    row0 = True
    users = {}
    for row in csvfile:
        if row0:
            row0 = False
            continue
        userid = row[3]
        post_tittle = row[6].replace(".", " . ").replace("!", " ! ").replace("?", " ? ")
        post_body = row[7]
        label = row[8]
        if label != outclass:
            continue


        txt = nltk.sent_tokenize(post_body.replace(".", " . ").replace("!", " ! ").replace("?", " ? "))
        tokeep = []
        for sent in txt:
            if len(sent.split()) > 3:
                tokeep.append(sent)
        outtxt = post_tittle + "\n" + "\n".join(tokeep)
        if userid not in users:
            users[userid] = outtxt
        else:
            users[userid] = users[userid] + "\n" + outtxt  + "\n"

    for userid in users:
        outfile = open(outfolder + "/" + userid, "w")
        outfile.write(users[userid])
        outfile.close()
    infile.close()

def get_test_set(filename:str, outfolder_prefix: str) -> None:
    get_test_set_worker(filename, outfolder_prefix + "_a", 'a')
    get_test_set_worker(filename, outfolder_prefix + "_b", 'b')
    get_test_set_worker(filename, outfolder_prefix + "_c", 'c')
    get_test_set_worker(filename, outfolder_prefix + "_d", 'd')

def get_training_set(path: str, filename_suffix: str, outfolder_prefix: str) -> None:
    get_training_set_worker(path + "/A" + filename_suffix, outfolder_prefix + "/A.txt")
    get_training_set_worker(path + "/B" + filename_suffix, outfolder_prefix + "/B.txt")
    get_training_set_worker(path + "/C" + filename_suffix, outfolder_prefix + "/C.txt")
    get_training_set_worker(path + "/D" + filename_suffix, outfolder_prefix + "/D.txt")

if __name__ == '__main__':
    get_training_set(argv[1], argv[2], argv[3])
    get_test_set(argv[4], argv[5])
