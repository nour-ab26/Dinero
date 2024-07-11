// Importing libraries that we installed using npm
const express = require("express");
const bcrypt = require("bcrypt");
const passport = require("passport");
//const initializePassport = require( "./config/passport").initialize;

const app = express();
const port=3000;
app.use(express.static(__dirname + '/public'));
app.use(express.urlencoded({extended:false}));  

// Routes
app.get('/', (req, res) => {
  res.render("acceuil.ejs");
})

app.get('/login', (req, res) => {
  res.render('login.ejs');
});

app.get('/homePage', (req, res) => {
  res.render('homePage.ejs');
});


app.get('/signUp', (req, res) => {
  res.render('signUp.ejs');
});

app.get('/transactions', (req, res) => {
  res.render('transactions.ejs');
});

app.get('/expense', (req, res) => {
  res.render('expense.ejs');
});

app.get('/income', (req, res) => {
  res.render('income.ejs');
});

app.get('/transafter', (req, res) => {
  res.render('transafter.ejs');
});

app.get('/budget', (req, res) => {
  res.render('budget.ejs');
});

app.get('/newbudget', (req, res) => {
  res.render('newBud.ejs');
});

app.get('/FoodBudget', (req, res) => {
  res.render('FoodBudget.ejs');
});

app.get('/bill', (req, res) => {
  res.render('bill.ejs');
});

app.get('/newbill', (req, res) => {
  res.render('newbill.ejs');
});

app.get('/ElecBill', (req, res) => {
  res.render('ElecBill.ejs');
});

app.get('/goal', (req, res) => {
  res.render('goal.ejs');
});

app.get('/newgoal', (req, res) => {
  res.render('newgoal.ejs');
});

app.get('/phonegoal', (req, res) => {
  res.render('phonegoal.ejs');
});

app.get('/dashboard', (req, res) => {
  res.render('dashboard.ejs');
});

app.get('/newAccount', (req, res) => {
  res.render('newAccount.ejs');
});

app.get('/addgoal', (req, res) => {
  res.render('addgoal.ejs');
});

app.get('/finalgoal', (req, res) => {
  res.render('finalgoal.ejs');
});
// End of routes

// In-memory
const users =[];

app.use(express.json());  // Middleware to parse JSON in the request body

app.post( "/signUp", async (req, res) => {   // Route for registration of new user
    try {
        const {firstName,lastName,email,password} = req.body ;     // Extract email and password from the request

       // Check if the user already exists
       const findUser = users.find((data) => email == data.email);
       if (findUser){
          res.status(400).send(" Wrong email or password !");
       }  

       // Hash password
       const hashedPassword = await bcrypt.hash(password,10);
       users.push({  id: Date.now().toString(), firstName, lastName, email, password:hashedPassword });
       console.log(users); // Display newly registered in the console
       //res.status(201).send("Registered successfully !");
       res.redirect("/login")
    } catch (err) {
          res.status(500).send({ message: err.message});
    }
});

app.post("/login",async (req,res)=>{      // Route for login authentication
    try{
      const {email,password}=req.body;

      // Find user
      const findUser = users.find((data) => email == data.email);
      if (!findUser){
        res.status(400).send(" Wrong email or password !");
      }

      // Compare passwords
      const passwordMatch =await bcrypt.compare(password,findUser.password);
      if (passwordMatch){
        //res.status(201).send("Logged in successfully !");
        res.redirect("/newAccount"); // Redirect to home page on successful login
      }else{ 
        res.status(400).send(" Wrong email or password !");}
    } catch (err){
        res.status(500).send({ message: err.message});
    }
});

app.listen(port, () => {
    console.log("Server is started on port 3000")
})
