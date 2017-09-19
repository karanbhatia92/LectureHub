import httplib, urllib, base64, json
def analyzesentiment( comment ) :
    sub_key = 'b117152ba2304ec4b5940ac81fc5e9dd'
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': sub_key,
    }

    body = {
      'documents': [
        {
          'language': 'en',
          'id': 'string',
          'text': comment
        }
      ]
    }

    params = urllib.urlencode({
    })

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/text/analytics/v2.0/sentiment?%s" % params, str(body), headers)
        response = conn.getresponse()
        data = response.read()
        jsondata = json.loads(data)
        score = jsondata['documents'][0]['score']
        conn.close()
        return round(score, 2)
    except Exception as e:
        print "Unexpected error:", e
        return
