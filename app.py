from website import create_app

app = create_app()

#If running file directly start flask
if __name__ == '__main__':
  #Run flask app, start web server 
  app.run(debug=True)
