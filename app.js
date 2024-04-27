// Importing libraries that we installed using npm
const express = require("express");
const bcrypt = require("bcrypt");


const app = express();
const port=3000;
app.use(express.static(__dirname + '/public'));

// Route to render homa page 
app.get('/', (req, res) => {
  res.render("acceuil.ejs");
})

// Route to render the login page
app.get('/login', (req, res) => {
  res.render('login.ejs');
});

// Route to render the signup page
app.get('/signUp', (req, res) => {
  res.render('signUp.ejs');
});

// In-memory
const users =[];

app.use(express.json());  // Middleware to parse JSON in the request body

app.post( "/signUp", async (req, res) => {   // Route for registration of new user
    try {
        const {email,password} = req.body ;     // Extract email and password from the request

       // Check if the user already exists
       const findUser = users.find((data) => email == data.email);
       if (findUser){
          res.status(400).send(" Wrong email or password !");
       }  

       // Hash password
       const hashedPassword = await bcrypt.hash(password,10);
       users.push({ email, password:hashedPassword });
       console.log(users);
       res.status(201).send("Registered successfully !");
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
        res.status(201).send("Logged in successfully !");
      }else{ 
        res.status(400).send(" Wrong email or password !");}
    } catch (err){
        res.status(500).send({ message: err.message});
    }
});

app.listen(port, () => {
    console.log("Server is started on port 3000")
})
