from flask import Flask, redirect, url_for, render_template, request, Response
import random
from cam import VideoCamera

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/db")
def db():
    return render_template("Dashboard.html")

@app.route("/services")
def service():
    return render_template("services.html")

@app.route('/exec1')
def parse1():
    return render_template("Crowd.html")

@app.route('/exec2')
def parse2():
    return render_template("occupancy.html")

@app.route('/exec3')
def parse3():
    return render_template("mask.html")

@app.route('/exec4')
def parse4():
    import attendance
    return render_template("services.html")

@app.route('/exec5')
def parse5():
    import appointment
    return render_template("services.html")


@app.route("/dash")
def dash():
    return render_template("dash.html")





@app.route('/cro1')
def parse6():
    import crowd_basic
    return render_template("Crowd.html")

@app.route('/cro2')
def parse7():
    import crowd_pro
    return render_template("Crowd.html")

@app.route('/crowd')
def pass1():
    return render_template("crowd1.html")







@app.route('/oc1')
def parse9():
    import occupancy_basic
    return render_template("occupancy.html")

@app.route('/oc2')
def parse10():
    import occupancy_pro
    return render_template("occupancy.html")








@app.route('/face1')
def parse11():
    import face_basic
    return render_template("mask.html")

@app.route('/face2')
def parse12():
    import face_pro
    return render_template("mask.html")

@app.route('/face3')
def parse13():
    import face_premium
    return render_template("mask.html")





@app.route('/real')
def real():
    return render_template("real.html")
def gen(cam):
    while True:
        #get camera frame
        frame = cam.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




@app.route('/cr1')
def cr1():
    import mall_analysis
    return render_template("crowd1.html")

@app.route('/cr2')
def cr2():
    import metro_analysis
    return render_template("crowd1.html")

@app.route('/cr3')
def cr3():
    import hotel_analysis
    return render_template("crowd1.html")

@app.route('/cr4')
def cr4():
    import busstop_analysis
    return render_template("crowd1.html")

@app.route('/cr5')
def cr5():
    import crowd_analysis
    return render_template("crowd1.html")

@app.route('/traj5')
def traj5():
    import movement_data_present
    return render_template("crowd1.html")

@app.route('/traj4')
def traj4():
    import bus_data_present
    return render_template("crowd1.html")

@app.route('/traj3')
def traj3():
    import hotel_data_present
    return render_template("crowd1.html")

@app.route('/traj2')
def traj2():
    import metro_data_present
    return render_template("crowd1.html")

@app.route('/traj1')
def traj1():
    import mall_data_present
    return render_template("crowd1.html")









if __name__ == "__main__":
    app.run(port=5000, debug=True)
