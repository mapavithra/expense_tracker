const firebaseConfig = {
    apiKey: "AIzaSyAAiLMYbuGQrYxVYpYyZCro6WkLgYxQM2g",
    authDomain: "expenseframework.firebaseapp.com",
    databaseURL: "https://expenseframework-default-rtdb.firebaseio.com",
    projectId: "expenseframework",
    storageBucket: "expenseframework.appspot.com",
    messagingSenderId: "70332761314",
    appId: "1:70332761314:web:ed52deec2604f510978abb"
  };

firebase.initializeApp(firebaseConfig);

var expenseFrameworkDB = firebase.database().ref("expenseFramework");

document.getElementById("expenseform").addEventListener("submit",submitForm);

function submitForm(e){
    //e.preventDefault();
    var email = getElementVal("email");
    var password = getElementVal("password");

    // console.log(email,password);
    saveMessages(email,password);

}

const saveMessages = (email,password)=>{
    var newExpenseFramework = expenseFrameworkDB.push();

    newExpenseFramework.set({
        email : email,
        password : password,
    });
};

const getElementVal = (id) =>{
    return document.getElementById(id).value;
}