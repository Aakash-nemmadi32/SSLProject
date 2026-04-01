#!/bin/bash

#this function hashes the password
hashed_password() {

     echo -n "$1" | sha256sum | awk '{print $1}'    
    
}

#this function checks whether The player is Not first time user or He is not in users.tsv
existence_of_user() {
      grep -q "^$1:" users.tsv      #returns 0 if pattern is matched otherwise 1 as exit status

}

#This function registers user in users.tsv if he is an First time player
user_registration() {
          local password="$2"
          local confirmpassword="$3"
          local  attempts_for_mismatches=2
        while(( attempts_for_mismatches >0 )) ; do
        if [[ "$password" == "$confirmpassword" ]] ; then #verifying His confirmpassword and Password are same
        hashedpassword=$( hashed_password "$password")
        echo "$1:$hashedpassword" >> users.tsv
        break
        else 
        echo "password and confirmpassword mismatched"
        read -s -p "player password: " password
        echo
        read -s -p "confirm player password: " confirmpassword
        echo
        ((attempts_for_mismatches--))
        if(( attempts_for_mismatches == 0 )) ; then
        echo "No Attempts left, Try again By running main.sh"
        exit 1
        fi
        fi
        done       
}

#This function authenticates user,Verify correct password for his username
authentication_user() {
        passwordinhash=$(hashed_password "$2" )
        stored_password=$( grep -E "^$1:" users.tsv | cut -d ":" -f 2 ) #stored Password in users.tsv
        if [[ $passwordinhash == $stored_password ]] ; then
        return 0
        else
        return 1
        fi
}

read -p "first player name: " player1
if existence_of_user "$player1" ; then           
read -s -p "first player password: " password1
echo
else
read -s -p "First player password: " password1
echo
read -s -p "confirm First player password: " confirmpassword1
echo
user_registration "$player1" "$password1" "$confirmpassword1"
fi
attempts_for_password_1=2
while (( attempts_for_password_1 > 0 )) ; do
if authentication_user "$player1" "$password1" ; then
read -p "Second Player name: " player2
if existence_of_user "$player2" ; then
read -s -p "Second player password: " password2
echo
else
read -s -p "Second player password: " password2
echo
read -s -p "confirm Second player password: " confirmpassword2
echo
user_registration "$player2" "$password2" "$confirmpassword2"
fi
attempts_for_password_2=2
while (( attempts_for_password_2 > 0 )) ; do
if authentication_user "$player2" "$password2" ; then
python3 game.py "$player1" "$player2"
exit 0
else
echo "incoorect password"
read -s -p "Second player password: " password2
echo
((attempts_for_password_2--))
fi
done
if (( attempts_for_password_2 == 0 )) ; then
echo " No Attempts Left,Try again by running main.sh"
exit 1
fi
else
echo "incorrect password"
read -s -p "First player password: " password1
echo
(( attempts_for_password_1--))
fi
done
if (( attempts_for_password_1 == 0 )) ; then
echo "No Attempts left,Try again by running main.sh"
exit 1
fi

