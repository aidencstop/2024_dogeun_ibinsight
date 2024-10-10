from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from member.models import *  # Importing CustomUser model from manager app
from manager.models import *
from forum.models import *

import os

def to_index(request):
    # Redirect to counselor-main page if user is already authenticated
    if request.user.is_authenticated:
        return redirect('to-main')

    # Handling form submission
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
            # Check if the user is a counselor
            print("user found !!")
            # Authenticate user
            authenticated_user = authenticate(request, username=username, password=password)
            print("user authenticated")

            # If authentication successful, login user
            if authenticated_user:
                print("user authenticated")
                login(request, authenticated_user)
                print("user logged in")
                return redirect('to-main')
            else:
                messages.error(request, "Invalid login credentials")
                print("Invalid credentials")
                return redirect('to-index')

        except CustomUser.DoesNotExist:
            # Handle non-existing user
            messages.error(request, "User does not exist")
            print("User does not exist")
            return redirect('to-index')

    return render(request, 'index.html', {})

def to_sign_up(request):
    # Handling form submission
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        year_of_graduation = request.POST.get('year_of_graduation')
        password = request.POST.get('password')
        password_confirm = request.POST.get('passwordconfirm')
        major = request.POST.get('major')
        interest = request.POST.get('interest')

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('to-sign_up')

        # Check if all required fields are filled
        if not all([username, password, password_confirm, name, year_of_graduation]):
            messages.error(request, "Please fill out all the required fields!")
            return redirect('to-sign_up')

        # Check if password matches confirm password
        if password == password_confirm:
            # Hash password and create new user
            hashed_password = make_password(password)
            new_user = CustomUser(
                username=username,
                name=name,
                year_of_graduation=year_of_graduation,
                password=hashed_password,
                major=major,
                interest=interest,
            )
            new_user.save()
            messages.success(request, "User added successfully!")
            return redirect('to-index')

        else:
            messages.error(request, "Password doesn't match. Please try again!")
            return redirect('to-sign_up')

    return render(request, 'signup.html')

@login_required
def to_main(request):
    if request.method == 'POST':
        major = request.POST.get('major')
        interest = request.POST.get('interest')

        curr_user = request.user

        curr_user.major = major
        curr_user.interest = interest

        curr_user.save()

        return redirect('to-main')

    curr_user = request.user
    all_post_list = [p for p in Post.objects.all().order_by('pk')]
    last_four_post_list = [p for p in reversed(all_post_list[-4:])]
    last_four_post_date_list = [p.created_at.strftime("%Y-%m-%d") for p in last_four_post_list]
    last_four_post_title_list = [p.title for p in last_four_post_list]
    last_four_post_pk_list = [p.pk for p in last_four_post_list]
    last_four_post_tuple_list = []
    for i in range(len(last_four_post_list)):
        last_four_post_tuple_list.append((last_four_post_date_list[i], last_four_post_title_list[i], last_four_post_pk_list[i]))
    post_list = [p for p in reversed(last_four_post_list)]

    from pathlib import Path
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent


    import pickle
    username = curr_user.username
    if os.path.isfile(os.path.join(BASE_DIR, 'static') + "/plot/" + username + '.pickle'):
        with open(file=os.path.join(BASE_DIR, 'static') + "/plot/" + username + '.pickle', mode='rb') as f:
            sl_hl_dict = pickle.load(f)
        sl_list = sl_hl_dict['sl']
        hl_list = sl_hl_dict['hl']
        hl_sl_tuple_list = []
        for i in range(len(sl_list)):
            hl_sl_tuple_list.append((hl_list[i], sl_list[i]))
    else:
        hl_sl_tuple_list = []

    context = {
        'curr_user': curr_user,
        'last_four_post_tuple_list': last_four_post_tuple_list,
        'post_list': post_list,
        'hl_sl_tuple_list': hl_sl_tuple_list,
    }

    return render(request, 'main.html', context)

@login_required
def to_about_ib(request):
    curr_user = request.user

    context = {
        'curr_user': curr_user,
    }
    return render(request, 'aboutib.html', context)

@login_required
def to_about_ib_course_search(request):
    group_list = Group.objects.all()
    course_list = Course.objects.all()

    group_id_list = []
    course_id_list = []
    course_name_list = []
    entry_guidance_list = []
    course_aim_list = []

    for course in course_list:
        group_id_list.append(course.group.id)
        course_id_list.append(course.id)
        course_name_list.append(course.name)
        entry_guidance_list.append(course.entry_guidance)
        course_aim_list.append(course.course_aims)

    curr_user = request.user

    context = {
        'curr_user': curr_user,
        'group_list': group_list,
        'course_list': course_list,
        'course_name_list': course_name_list,
        'group_id_list': group_id_list,
        'course_id_list': course_id_list,
        'entry_guidance_list': entry_guidance_list,
        'course_aim_list': course_aim_list,
    }
    return render(request, 'aboutibcoursesearch.html', context)

# View function for counselor logout
@login_required
def log_out(request):
    logout(request)
    return redirect('to-index')

def to_survey(request):
    if request.method == 'POST':

        nation = request.POST.get('nation')
        major = request.POST.get('major')
        grade = request.POST.get('grade')

        print(nation)
        print(major)
        print(grade)

        return redirect('to-survey')

    return render(request, 'survey.html', {})

def get_recommendation(IGCSE_grades, input_dict):
    import random
    # Full list of offered IB Subjects
    subject_list = [
        ["Maths AA SL", "Maths AA HL", "Maths AI SL", "Maths AI HL"], # ok
        ["Physics SL", "Physics HL", "Chem SL", "Chem HL", "Bio SL", "Bio HL", "CS SL", "CS HL", "ESS SL"],
        ["Econ SL", "Econ HL", "Geo SL", "Geo HL", "History SL", "History HL", "Psych SL", "Psych HL"],
        ["Korean A SL", "Korean A HL", "Spanish AB SL", "Spanish B SL", "Spanish B HL", "French AB SL",
         "French B SL", "French B HL", "Mandarin AB SL", "Mandarin B SL", "Mandarin B HL"],
        ["Eng A SL", "Eng A HL"], # ok
        ["Music SL", "Music HL", "Theatre SL", "Theatre HL", "Art SL", "Art HL", "Film SL", "Film HL"]
    ]

    # matrix corresponding to subject_list; 0 means not considered for recommendation
    subject_matrix = [
        [1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1],
        [0, 0, 0, 0, 0, 0, 1, 0]
    ]

    # Required subjects for different majors, if any
    sbjct_maths = ""
    sbjct_sci = ""
    sbjct_hum = ""
    sbjct_lang = ""
    sbjct_eng = ""
    sbjct_art = ""

    # subjects will be added here to check duplicates
    selected_subjects = []

    Sci_or_Engineering = False

    # Decide ESS; If bad grades in science, ESS gets confirmed
    if IGCSE_grades['Sciences'] != "a" and IGCSE_grades['Sciences'] != "a*":
        sbjct_sci = "ESS SL"
    else:
        subject_matrix[1][8] = 0

    # Eliminate subjects based on learning preference
    if input_dict["Learning_pref"] == "p":
        subject_matrix[1][3] = 0
        subject_matrix[1][5] = 0
    elif input_dict["Learning_pref"] == "m":
        subject_matrix[0][1] = 0
        subject_matrix[1][0] = 0
        subject_matrix[1][1] = 0

    # Decide whether to eliminate Maths AA HL
    if input_dict["AddMaths"] == "t":
        subject_matrix[0][0], subject_matrix[0][2], subject_matrix[0][3] = 0, 0, 0
        sbjct_maths = "Maths AA HL"
    elif input_dict["AddMaths"] == "f":
        subject_matrix[0][1] = 0

    # Decide which Humanities to eliminate; if not taken in IGCSE, HL can't be taken.
    if IGCSE_grades['Humanities'][0] == "e":
        subject_matrix[2][3] = 0
        subject_matrix[2][5] = 0
    elif IGCSE_grades['Humanities'][0] == "g":
        subject_matrix[2][1] = 0
        subject_matrix[2][5] = 0
    elif IGCSE_grades['Humanities'][0] == "h":
        subject_matrix[2][1] = 0
        subject_matrix[2][3] = 0

    # Decide which Arts to eliminate
    if IGCSE_grades['Arts'][0] == "a":
        subject_matrix[5][4], subject_matrix[5][5] = 1, 1
    if IGCSE_grades['Arts'][0] == "d":
        subject_matrix[5][2], subject_matrix[5][3] = 1, 1
    if IGCSE_grades['Arts'][0] == "m":
        subject_matrix[5][0], subject_matrix[5][1] = 1, 1
    if IGCSE_grades['English Lit'] == "a" or IGCSE_grades['English Lit'] == "a*":
        subject_matrix[5][7] == 1

    # CS
    if IGCSE_grades['AddSciorHum'][0] != "c":
        subject_matrix[1][6] = 0
        subject_matrix[1][7] = 0

    # countries
    if input_dict["Country"] == "g":
        if IGCSE_grades["Language"][0] == "k":
            subject_matrix[3][0], subject_matrix[3][1] = 1, 1
        elif IGCSE_grades["Language"][0] == "s":
            subject_matrix[3][3], subject_matrix[3][4] = 1, 1
        elif IGCSE_grades["Language"][0] == "f":
            subject_matrix[3][6], subject_matrix[3][6] = 1, 1
        elif IGCSE_grades["Language"][0] == "m":
            subject_matrix[3][9], subject_matrix[3][10] = 1, 1

    # Art related majors requires portfolios, so HL is almost necessary
    if input_dict["Major"] == "music":
        sbjct_art = "Music HL"
    elif input_dict["Major"] == "performingarts" or input_dict["Major"] == "theatre":
        sbjct_art = "Theatre HL"
    elif input_dict["Major"] == "art":  # Art HL needed for Art major
        sbjct_art = "Art HL"
    elif input_dict["Major"] == "film":
        sbjct_art = "Film HL"

    # Logic for UK
    elif input_dict["Country"] == "b":
        if input_dict["Major"] == "engineering":
            subject_matrix[0][0], subject_matrix[0][2], subject_matrix[0][
                3] = 0, 0, 0  # Exlude all math other than AA HL as its required
            sbjct_maths = "Maths AA HL"  # Required for most engineering
            sbjct_sci = "Physics HL"  # Required for most engineering
        if input_dict["Major"] in ["physics", "geophysics", "chemistry", "biology", "biochemistry"]:
            if "physics" in input_dict["Major"]:
                sbjct_sci = "Physics HL"  # required
            elif "chem" in input_dict["Major"]:
                sbjct_sci = "Chemistry HL"  # required
            elif "bio" in input_dict["Major"]:
                if sbjct_sci == "Chemistry HL":
                    sbjct_art = "Biology HL"  # sbjct_art is assigned since chemistry would be already assigned if the student wants to major in Biochemistry
                else:
                    sbjct_sci = "Biology HL"

        if input_dict["Major"] == "medicine":
            sbjct_sci = "Chemistry HL"
            sbjct_art = "Biology HL"

        if input_dict["Major"] == "economics":
            sbject_maths = "Maths AA HL"

        if input_dict["Major"] == "computerscience":  # Maths other than AI SL is required for CS
            subject_matrix[0][2] = 0

    elif input_dict["Country"] == "c":
        if "Engineering" in input_dict["Major"]:
            # Canada does not require SL or HL specifically hence random smaple
            sbjct_sci = random.sample(['Physics SL', 'Physics HL'], 1)[0]
            subject_matrix[1][0], subject_matrix[1][1] = 0, 0
            sbjct_art = random.sample(['Chemistry SL', 'Chemistry HL'], 1)[0]
            subject_matrix[1][2], subject_matrix[1][3] = 0, 0

    elif input_dict["Country"] == "u":
        pass

    # Secondary Language elimination for other than Germany
    if input_dict["Country"] != "g":
        if IGCSE_grades["Language"][0] == "k":
            subject_matrix[3][0] = 1  # Include Korean SL
            subject_matrix[3][2], subject_matrix[3][5], subject_matrix[3][8] = 1, 1, 1  # Include all language AB
        elif IGCSE_grades["Language"][0] == "s":
            subject_matrix[3][3] = 1  # Include Spanish SL
            subject_matrix[3][5], subject_matrix[3][8] = 1, 1  # Include other language AB
        elif IGCSE_grades["Language"][0] == "f":
            subject_matrix[3][6] = 1  # Include French SL
            subject_matrix[3][2], subject_matrix[3][8] = 1, 1  # Include other language AB
        elif IGCSE_grades["Language"][0] == "m":
            subject_matrix[3][9] = 1  # Include Mandarin SL
            subject_matrix[3][2], subject_matrix[3][5] = 1, 1  # Include other language AB

        if IGCSE_grades["Language"][1] == "9":
            subject_matrix[3][4], subject_matrix[3][7], subject_matrix[3][
                10] = 1, 1, 1  # Language HL shouldn't be taken unless very high grade in IGCSE
        elif IGCSE_grades["Language"][1] == "a*":
            subject_matrix[3][
                1] = 1  # Korean HL shouldn't be taken unless very high grade in Pre-IB (there is no "IGCSE" Korean)

    if input_dict["Major"]=="engineering" or input_dict["Major"] in ["physics", "geophysics", "chemistry",
                                                                       "biology", "biochemistry"]:
        Sci_or_Engineering = True

    Required_HL = []
    Required_SL = []

    Required_subjects = [sbjct_maths, sbjct_sci, sbjct_hum, sbjct_lang, sbjct_eng, sbjct_art]
    Required_sbjct_vec = [1, 1, 1, 1, 1, 1]  # sbjct vec matches the row indices of subject_list

    # make a list of required HL and SL subjects so far
    for index, sbjct in enumerate(Required_subjects):
        if "HL" in sbjct:
            Required_HL.append(sbjct)
            Required_sbjct_vec[index] = 0
            selected_subjects.append(sbjct)
        elif "SL" in sbjct:
            Required_SL.append(sbjct)
            Required_sbjct_vec[index] = 0
            selected_subjects.append(sbjct)

    print(f"Required_HL: {Required_HL} \nRequired_SL:{Required_SL} \nRequired Vector:{Required_sbjct_vec}")

    HL_Count = len(Required_HL)
    SL_Count = len(Required_SL)

    def is_duplicate_subject(chosen_subject):
        base_subject = chosen_subject.rsplit(' ', 1)[0]
        return any(base_subject in subject for subject in selected_subjects)

    while HL_Count < 3 or SL_Count < 3:
        for i in range(len(subject_list)):
            print(f"i: {i}")
            if Required_sbjct_vec[i] == 1:  # Check if the group still needs a subject
                if Sci_or_Engineering == True and i == 5:  # if major is science or engineering, instead of accessing the Arts subjects in subject_list, access Science subjects
                    i = 1

                available_subjects = [sub for j, sub in enumerate(subject_list[i]) if
                                      subject_matrix[i][j] == 1 and not is_duplicate_subject(sub)]
                print(f"available subjects: {available_subjects}")
                if len(available_subjects) > 0:
                    chosen_subject = random.choice(available_subjects)
                    print(f"Chosen subject {i + 1}: {chosen_subject}")
                if "HL" in chosen_subject and HL_Count < 3:
                    Required_HL.append(chosen_subject)
                    Required_sbjct_vec[i] = 0
                    HL_Count += 1
                    print(f"HL Count: {HL_Count}")
                    selected_subjects.append(chosen_subject)
                elif "SL" in chosen_subject and SL_Count < 3:
                    Required_SL.append(chosen_subject)
                    Required_sbjct_vec[i] = 0
                    SL_Count += 1
                    print(f"SL Count: {SL_Count}")
                    selected_subjects.append(chosen_subject)
                print(f"selected subjects:{selected_subjects}")
                print(
                    f"Required_HL: {Required_HL}, Required_SL:{Required_SL}, Required_sbjct_vec:{Required_sbjct_vec}")
                print(subject_matrix)

    print(f"Required_HL: {Required_HL}, Required_SL:{Required_SL}, Required_sbjct_vec:{Required_sbjct_vec}")

    Final_subjects = Required_HL + Required_SL
    print("final subjects:", Final_subjects)
    subject_list = [
        ["Maths AA SL", "Maths AA HL", "Maths AI SL", "Maths AI HL"],  # ok
        ["Physics SL", "Physics HL", "Chem SL", "Chem HL", "Bio SL", "Bio HL", "CS SL", "CS HL", "ESS SL"],
        ["Econ SL", "Econ HL", "Geo SL", "Geo HL", "History SL", "History HL", "Psych SL", "Psych HL"],
        ["Korean A SL", "Korean A HL", "Spanish AB SL", "Spanish B SL", "Spanish B HL", "French AB SL",
         "French B SL", "French B HL", "Mandarin AB SL", "Mandarin B SL", "Mandarin B HL"],
        ["Eng A SL", "Eng A HL"],  # ok
        ["Music SL", "Music HL", "Theatre SL", "Theatre HL", "Art SL", "Art HL", "Film SL", "Film HL"]
    ]
    final_subject_code_list = []
    for fs in Final_subjects:
        for i in range(len(subject_list)):
            if fs in subject_list[i]:
                final_subject_code_list.append(str(i)+str(subject_list[i].index(fs)))
    print("finial subjects codes:", final_subject_code_list)
    return Final_subjects, final_subject_code_list

def get_plot(username, code_list):
    # Libraries
    import matplotlib.pyplot as plt
    import pandas as pd
    from math import pi

    subject_list = [
        ["Maths AA SL", "Maths AA HL", "Maths AI SL", "Maths AI HL"],  # ok
        ["Physics SL", "Physics HL", "Chem SL", "Chem HL", "Bio SL", "Bio HL", "CS SL", "CS HL", "ESS SL"],
        ["Econ SL", "Econ HL", "Geo SL", "Geo HL", "History SL", "History HL", "Psych SL", "Psych HL"],
        ["Korean A SL", "Korean A HL", "Spanish AB SL", "Spanish B SL", "Spanish B HL", "French AB SL",
         "French B SL", "French B HL", "Mandarin AB SL", "Mandarin B SL", "Mandarin B HL"],
        ["Eng A SL", "Eng A HL"],  # ok
        ["Music SL", "Music HL", "Theatre SL", "Theatre HL", "Art SL", "Art HL", "Film SL", "Film HL"]
    ]


    # finial subjects codes: ['01', '51', '17', '26', '30', '40']
    g_dict = {
        '0': [], # Group 5
        '1': [], # Group 4
        '2': [], # Group 3
        '3': [], # Group 2
        '4': [], # Group 1
        '5': [], # Group 6
    }
    sl_list = []
    hl_list = []
    for code in code_list:
        target_g = code[0]
        if len(g_dict[target_g])==0:
            if subject_list[int(code[0])][int(code[1])][-2:]=="HL":
                g_dict[target_g] = [10]
                hl_list.append(subject_list[int(code[0])][int(code[1])])
            else:
                g_dict[target_g] = [5]
                sl_list.append(subject_list[int(code[0])][int(code[1])])
        else:
            if subject_list[int(code[0])][int(code[1])][-2:]=="HL":
                g_dict['5'] = [10]
                hl_list.append(subject_list[int(code[0])][int(code[1])])
            else:
                g_dict['5'] = [5]
                sl_list.append(subject_list[int(code[0])][int(code[1])])
    sl_hl_dict = {
        'sl': sl_list,
        'hl': hl_list,
    }


    from pathlib import Path
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    import pickle

    with open(file=os.path.join(BASE_DIR, 'static')+"/plot/"+username+'.pickle', mode='wb') as f:
        pickle.dump(sl_hl_dict, f)

    # Set data
    df = pd.DataFrame({
        'Group1: Studies in Language and Literature': g_dict['4'],
        'Group2: Language Acquisition': g_dict['3'],
        'Group3: Individuals and Societies (Humanities)': g_dict['2'],
        'Group4: Sciences': g_dict['1'],
        'Group5: Mathematics': g_dict['0'],
        'Group6: Arts': g_dict['5'],
    })

    # ------- PART 1: Define a function that do a plot for one line of the dataset!

    def make_spider(row, title, color):
        # number of variable
        categories = list(df)[0:]
        N = len(categories)

        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        # Initialise the spider plot
        ax = plt.subplot(2, 2, row + 1, polar=True, )

        # If you want the first axis to be on top:
        ax.set_theta_offset((pi / 6) * 2)
        ax.set_theta_direction(-1)

        # Draw one axe per variable + add labels labels yet
        plt.xticks(angles[:-1], [], color='grey', size=10)

        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([5, 10], ["", ""], color="grey", size=7)
        plt.ylim(0, 10)

        # Ind1
        values = df.loc[row].values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
        ax.fill(angles, values, color=color, alpha=0.4)

        # Add a title
        # plt.title(title, size=11, color=color, y=1.1)

    # ------- PART 2: Apply the function to all individuals
    # initialize the figure
    plt.figure(figsize=(20, 20), dpi=96, facecolor='#f7f7f7')

    # Create a color palette:
    my_palette = plt.cm.get_cmap("Set1", 20)

    # Loop to plot
    row = 0
    make_spider(row=row, title='group ', color=my_palette(0))



    plt.savefig(os.path.join(BASE_DIR, 'static')+"/plot/"+username+'.jpg', dpi=96, bbox_inches='tight')

def recommend(request):
    import random

    # TODO: Recommendation System Backend

    if request.method == 'POST':

        maths = request.POST.get('maths')
        addmaths = request.POST.get('addmaths')
        sciences = request.POST.get('sciences')
        englishlang = request.POST.get('englishlang')
        englishlit = request.POST.get('englishlit')
        language = request.POST.get('language')
        arts = request.POST.get('arts')
        humanities = request.POST.get('humanities')
        addsciorhum = request.POST.get('addsciorhum')
        country = request.POST.get('country')
        major = request.POST.get('major')
        learningpreference = request.POST.get('learningpreference')
        tookaddmaths = request.POST.get('tookaddmaths')

        # Dictionary of grades that the student will input on the website
        IGCSE_grades = {
            'Maths': maths, # a* / x
            'AddMaths': addmaths, # a* / x
            'Sciences': sciences, # a* / a / x
            'English Lang': englishlang, # a* / x
            'English Lit': englishlit, # a* / a / x
            'Language': [language[0], language[1:]], # k / s / f / m  a* / x / 9
            'Arts': [arts, arts], # a / d / m
            'Humanities': [humanities, humanities], # e / g / h
            'AddSciorHum': [addsciorhum, addsciorhum], # c / x
        }

        # Dictionary consisting of example answers to the questions on the website
        input_dict = {
            'Country': country,  # g/b/c/u which country to pursue university in?
            'Major': major,  # which major?
            'Learning_pref': learningpreference,  #  p/m problem solving or memorisation?
            'AddMaths': tookaddmaths,  # t/f Did you take additional maths?
        }

        subject_list, code_list = get_recommendation(IGCSE_grades, input_dict)

        curr_user = request.user
        username = curr_user.username

        get_plot(username, code_list)

        return redirect('to-main')
