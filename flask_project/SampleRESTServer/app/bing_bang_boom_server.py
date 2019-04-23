from flask import Flask

app = Flask(__name__)


@app.route('/api/v1/home')
def home_page():
    return "<h2><center>This is BingBangBoom Server</center></h2>"


@app.route('/api/v1/domain/<int:device_id>',)
def domain(device_id):
    if not device_id % 3 and device_id % 5:
        mapped_domain = "A"
        role = "Bing"
    elif device_id % 5 == 0 and device_id % 3:
        mapped_domain = "B"
        role = "Bang"
    elif not device_id % 3 and not device_id % 5:
        mapped_domain = "A and B"
        role = "Boom"
    else:
        mapped_domain = None
        role = "Meh"
    return "<h1><center>The mapped domain is : {} ,    And The role is : {}</center></h1>".format(mapped_domain, role)


if __name__ == "__main__":
    app.run(debug=True)
