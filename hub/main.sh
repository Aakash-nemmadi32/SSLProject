#!/bin/bash

# this function hashes the password using sha256
hashed_password() {
     echo -n "$1" | sha256sum | awk '{print $1}'        
}

# this function checks whether the player is a returning user or not
# returns 0 if found in users.tsv, 1 if not
existence_of_user() {
      grep -q "^$1:" users.tsv      # returns 0 if pattern is matched otherwise 1 as exit status
}

# this function registers a new player in users.tsv
# gives 2 chances to type matching passwords before quitting
user_registration() {
          local password="$2"
          local confirmpassword="$3"
          local attempts_for_mismatches=2

        while (( attempts_for_mismatches > 0 )) ; do
            if [[ "$password" == "$confirmpassword" ]] ; then   # passwords match, go ahead and save
                hashedpassword=$(hashed_password "$password")
                echo "$1:$hashedpassword" >> users.tsv
                break
            else 
                echo "password and confirmpassword mismatched"
                read -s -p "player password: " password
                echo
                read -s -p "confirm player password: " confirmpassword
                echo
                (( attempts_for_mismatches-- ))
                if (( attempts_for_mismatches == 0 )) ; then
                    echo "No Attempts left, Try again By running main.sh"
                    exit 1
                fi
            fi
        done       
}

# this function checks if the password the user typed matches what's stored
# returns 0 for correct, 1 for wrong
authentication_user() {
        passwordinhash=$(hashed_password "$2")
        stored_password=$(grep -E "^$1:" users.tsv | cut -d ":" -f 2)   # pull the stored hash from users.tsv
        if [[ $passwordinhash == $stored_password ]] ; then
            return 0
        else
            return 1
        fi
}

# -------- player 1 login / registration --------

read -p "first player name: " player1

if existence_of_user "$player1" ; then
    # returning user — just ask for password
    read -s -p "first player password: " password1
    echo
else
    # new user — ask for password and confirmation, then register
    read -s -p "First player password: " password1
    echo
    read -s -p "confirm First player password: " confirmpassword1
    echo
    user_registration "$player1" "$password1" "$confirmpassword1"
fi

# give player 1 two attempts to get their password right
attempts_for_password_1=2
while (( attempts_for_password_1 > 0 )) ; do
    if authentication_user "$player1" "$password1" ; then

        # -------- player 2 login / registration --------

        read -p "Second Player name: " player2

        if existence_of_user "$player2" ; then
            # returning user — just ask for password
            read -s -p "Second player password: " password2
            echo
        else
            # new user — ask for password and confirmation, then register
            read -s -p "Second player password: " password2
            echo
            read -s -p "confirm Second player password: " confirmpassword2
            echo
            user_registration "$player2" "$password2" "$confirmpassword2"
        fi

        # give player 2 two attempts to get their password right
        attempts_for_password_2=2
        while (( attempts_for_password_2 > 0 )) ; do
            if authentication_user "$player2" "$password2" ; then
                # both players authenticated — launch the game
                python game.py "$player1" "$player2"
                exit 0
            else
                echo "incoorect password"
                read -s -p "Second player password: " password2
                echo
                (( attempts_for_password_2-- ))
            fi
        done

        if (( attempts_for_password_2 == 0 )) ; then
            echo " No Attempts Left,Try again by running main.sh"
            exit 1
        fi

    else
        # player 1 typed the wrong password
        echo "incorrect password"
        read -s -p "First player password: " password1
        echo
        (( attempts_for_password_1-- ))
    fi
done

if (( attempts_for_password_1 == 0 )) ; then
    echo "No Attempts left,Try again by running main.sh"
    exit 1
fi
