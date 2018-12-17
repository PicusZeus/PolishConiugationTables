

"""
extracting list of lists of tuples (word, tags) from milionowy corpus.
Milionowy consists of various texts that are divided into a lot
of folders. Each of those folders include files with some particular
data that are named always in the same way.
Files named "ann_morphosyntax.xml" include data that are of interest to us.
Every text is here divided into sentences and then into words, and every word
is described with grammar tags.
This script is to extract all the data from this corpus that
can be used to feed NLTK perceptron.

Return - list of lists (sentences) of tuples (word, tag), that can be fed to Perceptron
"""

import glob, os
import xml.etree.ElementTree as ET

punctuation = {'...': 'ellipsis', '.': 'dot',',':'comma','?':'question mark',
                                    '!': 'exclamation mark',':': 'colon',
                                    ';':'semicolon','-':'hyphen' ,'(':'left parenthesis',
                                    ')':'right parenthesis', '“':'quotation left',
                                    '”': 'quotation right', '"': 'quotation' }

Milionowy = '.' # it is assumed that the script is run in the same directory that contains folders
                # from milionowy

def extractor(folder = Milionowy):

    listOfTaggedWords = []
    # make a list of all the folders
    os.chdir(folder)
    curdir = os.getcwd()
    directories = [i for i in glob.glob('*') if os.path.isdir(i)]
    full_dir_names = [os.path.join(curdir, i) for i in directories]


    for folder in full_dir_names:

        file = os.path.join(folder, 'ann_morphosyntax.xml')
        if os.path.isfile(file):

            tree = ET.parse(file)
            root = tree.getroot()

            # root[1] - teiCorpus
            # root[1][1][0] - body - it consists of sentences

            for sentence in root[1][1][0]:
                # sentence[0][0] consists of words
                sent = []
                for word in sentence[0]:


                    logos = word[0][0][0].text



                    tag = word[0][2][0][1][0].text
                    # tag has this kind of structure:
                    # chodzić:fin:sg:ter:imperf
                    # extract only grammar info
                    if tag:
                        tag = ",".join(tag.split(':')[1:])

                    # puctuation marks will be dealt here

                    if logos in punctuation.keys():
                        tag = logos


                    # for some reason punctuation marks and
                    # some other words have additional field
                    # <f name="nps">
                    # <binary value="true"/>
                    # < /f>
                    # and so node with grammsr
                    # info is moved one step further.
                    # If this is the case the grammar info is taken from here
                    if tag == None:
                        tag = word[0][3][0][1][0].text
                        tag = ",".join(tag.split(':')[1:])

                    sent.append((logos, tag))
                listOfTaggedWords.append(sent)


    return listOfTaggedWords





"""
An example of parsed xml


<fs type="morph">
    <f name="orth">
        <string>Close</string>
    </f>
    <!-- Close [11,5] -->
    <f name="nps">
        <binary value="true"/>
    </f>
    <f name="interps">
        <fs type="lex" xml:id="morph_6.4.1-lex">
            <f name="base">
                <string/>
            </f>
            <f name="ctag">
                <symbol value="ign"/>
            </f>
            <f name="msd">
                <symbol value="" xml:id="morph_6.4.1.1-msd"/>
            </f>
        </fs>
        <fs type="lex" xml:id="morph_6.4.3-lex">
            <f name="base">
                <string>close</string>
            </f>
            <f name="ctag">
                <symbol value="subst"/>
            </f>
            <f name="msd">
                <symbol nkjp:manual="true" value="sg:acc:n" xml:id="morph_6.4.3.1-msd"/>
            </f>
        </fs>
    </f>
    <f name="disamb">
        <fs feats="#an8003" type="tool_report">
            <f fVal="#morph_6.4.3.1-msd" name="choice"/>
                <f name="interpretation">
                    <string>close:subst:sg:acc:n</string>
"""
