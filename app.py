from flask import render_template, Flask, request
import boto3
import botocore
import json


app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET',"POST"])
def splash():
    return render_template('./splash.html')

@app.route('/index.html', methods=['GET',"POST"])
def home():
    return render_template('./index.html')

@app.route('/configureStack.html')
def configure():
    return render_template('./configureStack.html')

@app.route('/deployStack.html')
def deploy():
    return render_template('./deployStack.html')

@app.route('/existingStack.html')
def existing():
    return render_template('./existingStack.html')

def launchStack():
    if request.method == "POST":
        with open("create.json") as f:
            data = json.load(f)
        data['Parameters']['KeyName']['Default'] = request.form.get("keypair")
        data['Parameters']['DBName']['Default'] = request.form.get("dbname")
        data['Parameters']['SSHLocation']['Default'] = request.form.get("sshloc")
        data['Parameters']['DBUser']['Default'] = request.form.get("dbuser")
        data['Parameters']['DBPassword']['Default'] = request.form.get("dbpassword")
        data['Parameters']['DBRootPassword']['Default'] = request.form.get("dbrootpassword")
        data['Parameters']['InstanceType']['Default'] = request.form.get("instType")
        print(data)
        client = boto3.client('cloudformation',
            region_name = 'ap-east-1',
            aws_access_key_id='aws_access_key_id',
            aws_secret_access_key='aws_secret_access_key')
        response = client.create_stack(
            StackName=request.form.get("sname"),
            TemplateBody=json.dumps(data),
            DisableRollback=False,
        )

    return response


if __name__ == "__main__":
    app.run()