from flask import render_template, flash, redirect,url_for, g, request
from urllib.parse import urlparse,urlunparse
from app import app,db,lm
from .forms import LoginForm,ForgotForm, PostForm,SuggestForm,NewPasswordForm,EditForm
from flask.ext.login import login_user, logout_user,\
    current_user, login_required
from datetime import datetime
from .models import User, Posting, Suggestion
from flask.ext.sqlalchemy import get_debug_queries
from config import DATABASE_QUERY_TIMEOUT
import stripe
from .token import generate_confirmation_token, confirm_token
from .emails import send_email
from .decorators import check_confirmed
from .domain import checkDomain

stripe_keys = {
    'secret_key': 'sk_test_n8bhCzBDGLxqbPfCoz7HYeQl',
    'publishable_key': 'pk_test_n00tOVxN8YpmQphYGRVclqLe'
}

stripe.api_key = stripe_keys['secret_key']

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user   
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()    
    urlparts = urlparse(request.url)
    flash("1")    
    flash(urlparts)
    change=False
    if urlparts.netloc == 'namegeniuses.com':
        urlparts_list = list(urlparts)
        urlparts_list[1] = 'www.namegeniuses.com'
        flash('1')
        urlparts=urlunparse(urlparts_list)
        change=True
    if urlparts.scheme == 'http':
        if change==True:
            urlparts = urlparse(urlparts)
        urlparts_list = list(urlparts)
        urlparts_list[0] = 'https'
        urlparts=urlunparse(urlparts_list)
        change=True
    flash("2")
    flash(change)
    flash(urlparts)
    change=False
    if change==True:
        return redirect(urlparts,code=301)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           title='Home',
                           defaultfooter=True)
                           
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
@check_confirmed
def dashboard():
    user = g.user
    current_postings = Posting.query.filter_by(user_id=user.id).all()
    allpostings=Posting.query.all()
    current_suggestions=Suggestion.query.filter_by(suggester=user.id).all()
    counter=0
    for s in current_suggestions:
        counter+=1
    currentwins=user.wins
    winnings=user.totalwinnings        
    return render_template('dashboard.html',
                           title='Dashboard',
                           user=user,
                           projects=current_postings,
                           suggestions=current_suggestions,
                           count=counter,
                           currentwins=currentwins,
                           winnings=winnings,
                           allpostings=allpostings
                           )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('dashboard'))
    form=LoginForm()
    if form.validate_on_submit():
        username = form.email.data
        password = form.password.data
        user=User.query.filter_by(email=username).first()
        if user is None:
            flash("You haven't registered yet")
            return redirect(url_for('login'))            
        if user.is_correct_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Incorrect username or password")
            return redirect(url_for('login'))                        
    return render_template('login.html', 
                           title='Sign In',
                           form=form)
                           
@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    form=ForgotForm()     
    if form.validate_on_submit():
        email = form.email.data
        user=User.query.filter_by(email=email).first()
        if user is None:
            flash("There is no user with this email address")
            return render_template('forgotpassword.html', 
                       title='Forgot Password',
                       form=form)
        else:           
            token = generate_confirmation_token(user.email)
            flash('An email has been sent to your email address!')
            reset_url = url_for('newpassword', token=token, _external=True)
            html = render_template('passwordemail.html', reset_url=reset_url)
            subject = "Your password resetting instructions"
            send_email(user.email, subject, html)             
    return render_template('forgotpassword.html', 
                           title='Forgot Password',
                           form=form)         

@app.route('/newpassword/<token>', methods=['GET', 'POST'])
def newpassword(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first()
    form=NewPasswordForm()     
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash("Your password has been changed successfully!")
        return redirect(url_for('login'))                        
        
    return render_template('newpassword.html', 
                           title='Choose your new password',
                           form=form) 
                           
@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('dashboard'))
    form=LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        pw= form.password.data
        user=User.query.filter_by(email=email).first()
        if user is None:
            user=User(email=email,password=pw,jobposter=True,paypalemail=email)
            db.session.add(user)
            db.session.commit()
            
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)                        
            
            login_user(user, True)
            return redirect(url_for('unconfirmed'))            
        if user.is_correct_password(pw):
            login_user(user)
            return redirect(url_for('dashboard'))        
        else:
            flash("Username exists, but not with that password")
            return redirect(url_for('dashboard'))        

    return render_template('register.html', 
                           title='Register',
                           form=form)

@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed is True:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.timestamp = datetime.utcnow()
        db.session.commit()
        if user.jobposter==True:
            html = render_template('welcome.html')
            subject = "Welcome to Name Geniuses - Here's how to get started"
            send_email(user.email, subject, html)   
        else:
            html = render_template('welcomesugg.html')
            subject = "Welcome to Name Geniuses - Here's how to get started"
            send_email(user.email, subject, html)   
        
        flash('You have confirmed your account. Thanks!', 'success')
        
    return redirect(url_for('index'))

@app.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('unconfirmed'))
    


@app.route('/newproject', methods=['GET', 'POST'])
@login_required
@check_confirmed
def newproject():
    form=PostForm()
    if form.validate_on_submit():
        title = form.title.data
        description= form.description.data
        anyelse=form.Anything_else.data
        typestring=form.project_type.data
        project_type=typestring.split(" ")
        if project_type[0]=="The":
            project_type="The Motivator"
        else:
            project_type="Basic"
        time=datetime.utcnow()
        timeday=time.date()
        project=Posting(title=title, anything_else=anyelse, description=description, creator=g.user, timestamp=time, timestamp_day=timeday, project_type=project_type)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('newproject.html', 
                           title='Create a new project',
                           form=form)
                                  
@app.route('/project/<pnumber>')
def projectpage(pnumber):
    user=g.user
    projectdata = Posting.query.filter_by(id=pnumber).first()
    suggestdata= Suggestion.query.filter_by(posting_id=pnumber).all()
    winstatus=Suggestion.query.filter_by(posting_id=pnumber).filter_by(winstatus=True).first()
    if winstatus:
        winnerchosen=True
    else:
        winnerchosen=False
    return render_template('projectpage.html',
                           user=user,
                           pdata=projectdata,
                           suggestdata=suggestdata,
                           winnerchosen=winnerchosen,
                           winstatus=winstatus,
                           title="Project details")

@app.route('/postings')
def postings():
    allprojects = Posting.query.filter_by(status="Live").all()
    closedprojects = Posting.query.filter_by(status="Closed").all()    
    return render_template('allprojects.html',
                           allprojects=allprojects,
                           closedprojects=closedprojects,
                           title="All projects")

@app.route('/pickwinner/<pnumber>/<suggest>/<suggnumber>')
@login_required
@check_confirmed
def pickwinner(pnumber,suggest,suggnumber):
    user=g.user
    #get the project entry
    project = Posting.query.filter_by(id=pnumber).first()
    if project.winner:
        flash("You've already picked a winner")
        return redirect(url_for('projectpage', pnumber=pnumber))
    #checks if current user (the project poster) is equal to the project poster; just to ensure no one else is able to pick a winner
    if user.id==project.user_id:
        winner=Suggestion.query.filter_by(id=suggest).first()
        winner.winstatus=True
        project.status="Closed"
        if suggnumber=="1":
            project.winner=winner.Suggest1
        if suggnumber=="2":
            project.winner=winner.Suggest2
        if suggnumber=="3":
            project.winner=winner.Suggest3
        if suggnumber=="4":
            project.winner=winner.Suggest4
        if suggnumber=="5":
            project.winner=winner.Suggest5
        #add the win to the suggester
        winningsuggester=User.query.filter_by(id=winner.suggester).first()
        winningsuggester.wins+=1
        if project.project_type=="Basic":
            winningsuggester.totalwinnings+=16
        else:
            winningsuggester.totalwinnings+=46
        db.session.commit()
    return redirect(url_for('dashboard'))



@app.route('/suggest/<pnumber>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def suggest(pnumber):
    user=g.user
    form=SuggestForm()
    projectdata = Posting.query.filter_by(id=pnumber).first()
    if form.validate_on_submit():
        prevsugg=Suggestion.query.filter_by(suggester=user.id).filter_by(posting_id=pnumber).first()
        try:
            if prevsugg.Suggest5:
                flash("You've already made 5 suggestions for this project (the maximum allowed), please pick a different one")
                return redirect(url_for('dashboard'))
        except:
            pass
        Suggest1 = form.Suggest1.data
        Suggest2 = form.Suggest2.data
        Suggest3 = form.Suggest3.data
        Suggest4 = form.Suggest4.data
        Suggest5 = form.Suggest5.data
        badnames=[]
        count=0
        if Suggest1:        
            count+=1
            if not checkDomain(Suggest1):
                badnames.append(Suggest1)
        if Suggest2: 
            count+=1            
            if not checkDomain(Suggest2):
                badnames.append(Suggest2)
        if Suggest3:     
            count+=1
            if not checkDomain(Suggest3):
                badnames.append(Suggest3)
        if Suggest4:     
            count+=1
            if not checkDomain(Suggest4):
                badnames.append(Suggest4)
        if Suggest5:     
            count+=1
            if not checkDomain(Suggest5):
                badnames.append(Suggest5)
        if badnames:
            return render_template('suggestion.html',
                           form=form,
                           badnames=badnames,
                           pdata=projectdata,
                           title="Make a suggestion")       
        try:
            if prevsugg.Suggest1:
                secondcount=0
                list1=[prevsugg.Suggest1,prevsugg.Suggest2,prevsugg.Suggest3,prevsugg.Suggest4,prevsugg.Suggest5]
                for l in range(4,-1,-1):
                    if len(list1[l])<3:
                        del list1[l]
                list2=[Suggest1, Suggest2,Suggest3, Suggest4, Suggest5]
                list3=list1+list2
                for domain in list3:
                    if len(domain)>2:
                        secondcount+=1
                fulllist=secondcount-len(list1)
                prevsugg.Suggest1=list3[0]
                prevsugg.Suggest2=list3[1]
                prevsugg.Suggest3=list3[2]
                prevsugg.Suggest4=list3[3]
                prevsugg.Suggest5=list3[4]
                projectdata.number_of_entries+=fulllist
                db.session.commit()
        except:
            time=datetime.utcnow()
            timeday=time.date()
            Suggestions=Suggestion(Suggest1=Suggest1, Suggest2=Suggest2,Suggest3=Suggest3,Suggest4=Suggest4,Suggest5=Suggest5, poster=projectdata, suggester=user.id, timestamp=time, timestamp_day=timeday)
            projectdata.number_of_entries+=count            
            db.session.add(Suggestions)
            db.session.commit()
        flash('Your suggestions have been submitted!')
        return redirect(url_for('projectpage',pnumber=projectdata.id))
    return render_template('suggestion.html',
                           form=form,
                           pdata=projectdata,
                           title="Make a suggestion")

@app.route('/becomesuggester', methods=['GET', 'POST'])
def suggester():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('becomesuggester.html', 
                           title='Become a suggester')

@app.route('/registersuggester', methods=['GET', 'POST'])
def registersuggester():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('dashboard'))
    form=LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        pw= form.password.data
        user=User.query.filter_by(email=email).first()
        if user is None:
            user=User(email=email,password=pw,suggester=True,paypalemail=email)
            db.session.add(user)
            db.session.commit()

            token = generate_confirmation_token(user.email)
            flash('Your account has been created!')
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)                           
        
            login_user(user, True)
            return redirect(url_for('dashboard'))            
        if user.is_correct_password(pw):
            login_user(user)
            return redirect(url_for('dashboard'))        
        else:
            flash("Username exists, but not with that password")
            return redirect(url_for('dashboard'))   
    return render_template('registersuggester.html', 
                           title='Register as a suggester',
                           form=form)

@app.route('/charge/<projectid>/<amount>', methods=['POST'])
@login_required
@check_confirmed
def charge(projectid,amount):
    # Amount in cents
    realamount=int(float(amount)*100)
    user=g.user
    customer = stripe.Customer.create(
        email=user.email,
        card=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=realamount,
        currency='usd',
        description='Charge for name suggestions'
    )
    Projectrecord=Posting.query.filter_by(id=projectid).first()
    Projectrecord.status="Live"
    db.session.commit()    
    flash("Payment successful, your project is live!")
    return redirect(url_for('dashboard'))  

@app.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile():
    form=EditForm()
    user=g.user
    if form.validate_on_submit():
        email = form.paypalemail.data
        user.paypalemail=email
        db.session.commit()
        return redirect(url_for('dashboard'))
  
    return render_template('editprofile.html', 
                           title='Edit Profile',
                           form=form)
                                                      
@app.route('/payment/<ptype>/<pid>', methods=['GET', 'POST'])
def payment(pid, ptype):
    key=stripe_keys['publishable_key']
    if ptype=="Basic":
        amount="20.00"
        centsamount="2000"
    else:
        amount="50.00"
        centsamount="5000"
    return render_template('payment.html', amount=amount, centsamount=centsamount,key=key, projectid=pid, title="Payment")

@app.route('/pricing')
def pricing():
    return render_template('pricing.html', title="Pricing")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed is True:
        return redirect(url_for('index'))
    return render_template('unconfirmed.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
        
@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (query.statement, query.parameters, query.duration, query.context))
    return response
    
