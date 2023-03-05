from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
import csv
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app=Flask(__name__)

@app.route('/', methods= ['GET'])
def renderTemplate():
    return render_template("index.html")


@app.route('/review', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            print(prod_html)
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})

            
            reviews = []
            for commentbox in commentboxes:
                try:
                    #name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text

                except:
                    name = 'No Name'
                    logging.info("name")

                try:
                    #rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text


                except:
                    # rating = 'No Rating'
                    logging.info("rating")

                try:
                    #commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    # commentHead = 'No Comment Heading'
                    logging.info("commentHead")
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    #custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text
                except Exception as e:
                    # print("Exception while creating dictionary: ",e)
                    logging.info(e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)
                logging.info("log my final result {}".format(reviews))

                
            keys = reviews[0].keys()

            with open('reviews.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(reviews)
  
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            # print('The Exception message is: ',e)
            logging.info(e)

            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__=="__main__":
    # app.run(host="127.0.0.1",port=5000)
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)



# def welcome():
#     searchingString = "iphone11"
#     flipkart_url  = "https://www.flipkart.com/search?q=" + searchingString

#     uclient = uReq(flipkart_url)

#     flipkartPage =  uclient.read()

#     flipkart_html = bs(flipkartPage, "html.parser")
#     # test = flipkart_html.prettify()

#     bigBoxes=flipkart_html.findAll("div",{"class":"_1AtVbE col-12-12"})
#     # len(bigBoxes)
#     # bigBoxes[0]
#     box = bigBoxes[2]
#     # str(box.div.div.div)
#     productLink = 'https://www.flipkart.com'+ box.div.div.div.a['href']
#     productreq = requests.get(productLink)

#     # it will return 200 response if every thing is ok
#     # productreq 


#     # it will return all html data
#     # productreq.text

#     prod_html = bs(productreq.text,"html.parser")

#     comment_box = prod_html.find_all("div", {"class" : "_16PBlm"})

#     for i in comment_box:
#         print(i.div.div.div.text)
#     # return str(len(comment_box))





# if __name__=="__main__":
#     app.run(host="127.0.0.1",port=5000)