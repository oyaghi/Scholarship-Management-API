# Project

Project Description

<em>[TODO.md spec & Kanban Board](https://bit.ly/3fCwKfM)</em>

### Todo

- [ ] Implements Throttle for Provider, Seeker, Anonomos Users (OPTIONAL)  
- [ ] Implement Pagination on Functions the has the GET method (OPTIONAL)  
- [ ] LOGOUT (Tell the Front-end to implement a button that clear the stored token, and then redirect the user to the login page)  
- [ ] New Function ( Give the token expiry a small duration and when the client makes a new api call then the expiry will be reset, if  he makes an api call when the token is expired he will be logged out and will be forced to login AGAIN )  
- [ ] Modify the "Update"  API so that it can display the specific Error/Exception in the data validation.  

### In Progress

- [ ] Implement Email Verfication  

### Done ✓

- [x] Edit the "add_view" function, the problem is with the GET since it needs a Provider Token in order to function, Eliminate the Token Needs, since the api call should be something casual  
- [x] Add "FavList" which will view all the views that the Seeker Added to Favorite  
- [x] implement "Favorit Scholarship" for Seeker (OPTIONAL)  
- [x] Add "Add to Favorite" which will take the scholarship id and the seeker id and then add the scholarship to the "FavList" that belongs to the seeker  
- [x] Access the new table (many-to-many) relashinship by using the "through" keyward  
- [x] Test the Add,Delete,Update Scholarship  
- [x] update the "scholar_link" field, and make it HttpField  
- [x] update the start_date and end_date in Scholarship model  
- [x] Update the "view scholarship" so it can view the email and the full name of the provider with the scholarship  
- [x] Update to the "add" scholarship to fetch the id of the providere based on the token that will be sent  
- [x] create the update scholarship for provider  
- [x] create the delete scholarship for provider  

