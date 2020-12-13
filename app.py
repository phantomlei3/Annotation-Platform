from flask import Flask, redirect, url_for, render_template, request, session
from batches import Batch
import sys

app = Flask(__name__)

app.secret_key = "annotation"


example_string = '''
111Flu season has arrived, just as it has every year prior. But somehow, the flu is suddenly a more intense life-threatening situation than in decades past. That is to say, the news is completely unhinged in its flu reporting strategy.
'''

@app.route('/', methods=["GET"])
def start():
    session["batch_id"] = "test"
    batch = Batch(session["batch_id"])
    session["paragraph_id"] = batch.get_first_paragraph_id()

    return redirect(url_for("annotation_page"))

@app.route('/annotation', methods=["POST", "GET"])
def annotation_page():

    # post request to store annotations in PostgreSQL table
    if request.method == "POST":
        # batch information for the annotated information
        batch_id = session["batch_id"]
        annotated_paragraph_id = session["paragraph_id"]

        ## TODO: temporary variables for collecting annotations in category4.html
        exemption_label = request.form["exists"]
        categories = request.form.getlist("category")
        # variable to store all annotations
        annotations = list(exemption_label) + categories

        # save annotations in PostgreSQL
        batch = Batch(batch_id)
        batch.save_annotation(annotated_paragraph_id, annotations)

        # jump to next annotation page
        next_paragraph_id = batch.get_next_paragraph_id(annotated_paragraph_id)

        # No paragraph left in this batch
        if next_paragraph_id is None:
            session["paragraph_id"] = "None"
            return "Finished"
        else:
            session["paragraph_id"] = next_paragraph_id
            paragraph = batch.get_paragraph(next_paragraph_id)
            return render_template("category4.html", paragraph=paragraph)

    # get request to create the page for annotation
    if request.method == "GET":
        ## TODO: TESTING
        batch_id = session["batch_id"]
        batch = Batch(batch_id)
        # Batch annotations are not finished
        if session["paragraph_id"] == "None":
            return "Finished"
        else:
            paragraph = batch.get_paragraph(session["paragraph_id"])
            return render_template("category4.html", paragraph=paragraph)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000", debug=True)
