#!/bin/bash
#Run docker:
#  docker-compose build
#  docker-compose up

function clean {
    rm -rf static/sounds/words/*
    rm -rf static/sounds/examples/*
}

function run_test {
    name=$1
    checks=$2
    send=$3
    method=$4
    data=$5

    if [[ ${method} == 'POST' ]]; then
        curl -s -d ${data} ${send} > /dev/null
    else
        curl -s ${send} > /dev/null
    fi

    for item in ${checks[*]}; do
        if [[ -z $(ls ${check}) ]]; then
            echo "${name} - [ ERROR ]"
            exit 1
        fi
    done

    echo "${name} - [ OK ]"
}

clean
run_test "Test download word with GB voice" "static/sounds/words/car-gb.mp3" "http://localhost:5000/download/word?text=car&voice=en-GB" && clean
run_test "Test download word with US voice" "static/sounds/words/car-us.mp3" "http://localhost:5000/download/word?text=car&voice=en-US" && clean
run_test "Test download sentence with GB voice" "static/sounds/examples/33bb93a69278c6a00b0215ec91e1a911.mp3" "http://localhost:5000/download/sentence" "POST" "text=Hello%20world&voice=en-GB" && clean
run_test "Test download sentence with US voice" "static/sounds/examples/d389c5d2de592fe40af4355aa20e88bc.mp3" "http://localhost:5000/download/sentence" "POST" "text=Hello%20world&voice=en-US" && clean

hello_word_data=(static/sounds/examples/1881ad121c8b7ebb6551e1dd0566f494.mp3  static/sounds/examples/9b72d34358a3ae6322c4b051fa9b92ef.mp3
static/sounds/examples/298a0d8af2042299691354cb06f55e09.mp3  static/sounds/examples/ca6e1232e0819963c8a22f0492708e45.mp3
static/sounds/examples/31f7b2f3ca16475f76868bfd6569b906.mp3  static/sounds/examples/daada77b5525041dd5884029018de5ef.mp3
static/sounds/examples/6be6ab498498612ae4babff9dff371fc.mp3  static/sounds/examples/df36a2c66f6b374b2f6b4cd2f418bd06.mp3
static/sounds/words/hello-gb.mp3  static/sounds/words/hello-us.mp3)

clean
run_test "Test download all word data" "${hello_word_data[*]}" "http://localhost:5000/download/word/all?text=hello" 
run_test "Test download all word data again" "${hello_word_data[*]}" "http://localhost:5000/download/word/all?text=hello" 
clean

echo ''
echo 'Test Microsoft translator:'
echo $(curl -s localhost:5000/translate -d 'text=hello&engine=microsoft&from=en&to=cs') === '{"result":"dobr\u00fd den","status":200}'
echo ''
echo 'Test Google translator:'
echo $(curl -s localhost:5000/translate -d 'text=hello&engine=google&from=en&to=cs') === '{"result":"Ahoj","status":200}'
echo ''
