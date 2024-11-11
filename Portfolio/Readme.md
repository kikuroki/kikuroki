# 🗺 Oleksii's Portfolio

Welcome to my portfolio! Here, I document a summary of my projects in the data field. 

## 📚 Table of Contents

- 🐍[Python Developer](#python-developer-at-coltrans-sp-z-oo)
- 🐢[PET Projects](#data-science-pet-projects)

# 🐍Python Developer (at Coltrans sp. z o.o.)

### Context: 
During my work, I implemented several pilot projects under NDA with limited deadlines (1-2 weeks for each), aimed at creating prototypes for the company's internal needs. To quickly launch the functionality under strict deadlines and minimal resources, it was decided to use Google API and Google Sheets. This approach allowed colleagues from logistics, with whom I had previously worked as a logistician, to easily master the tool and start using it.

At all stages of the project, I acted independently: debugged, tested, organized feedback with end users and discussed the development plan with the manager. Debugging sometimes took place in real-time, during active product use, ensuring immediate issue resolution and minimal disruption.

For access to APIs from third-party providers such as Timocom, Transporeon and Trans.eu (platforms for loads matching), I also personally negotiated, which contributed to the successful integration of the necessary data into the project.

This portfolio illustrates my comprehensive approach to completing tasks, including planning, technical implementation, user interaction, and working in a fast-paced environment.



| Project Link | Tools | Libraries | Project Description |
|---|---|---|---|
| 📊🚚 Automated Loads Market Analysis  | Python, SQLite, Google Sheets, Googel API, GeoNames API | pandas, numpy, requests, imaplib, smtplib, threading, asyncio | The project allowed the company to analyze loads market offers by integrating data from Transporeon and automating updates on the Timocom platform. In Google Sheets, users could easily select parameters to filter by basic trip data, which provided flexibility in the analysis. Each row in the main sheet represented a separate data set, available for a more detailed view in a separate tab, where the data was updated in real time, and outdated data was marked as irrelevant. In addition, a tab was created with parameters for initial sorting, such as status (e.g. deleted or changed data), so that users could customize the initial data filtering to their needs. |
| 🗺️📤Automated Loads Publishing |  Python, SQLite, Postman API, Google Sheets, Googel API, GeoNames API | pandas, numpy, requests, imaplib, smtplib, threading, asyncio | The project allowed the company's logisticians to centrally publish loads on Timocom and Trans.eu, using Google Sheets to enter basic trip data. To save money, integration with Trans.eu was set up via Postman and the Postman API to obtain API keys, which bypassed the need to use an callback URL for extra cost. Also, to bypass API limitations, a user rotation system was implemented, which automatically distributed routes between accounts, ensuring stability of work and effective load management. |
| 🔍✉️Automated Loads Search | Python, SQLite, Google Sheets, Googel API, GeoNames API | pandas, numpy, requests, imaplib, smtplib, threading, asyncio | This project automated the route search process for logisticians on Timocom, allowing to set search parameters, such as start and end points (optionally including a radius of up to 100 km) and dates. The program automatically generated the text of the message on behalf of the user who set the parameters, for the owner of the suitable route. Due to API limitations, all messages were sent from one email address, so a forwarding system was implemented: using metadata and mail content analysis, the program determined to which of the logisticians the response was addressed and forwarded it, which ensured high accuracy and convenience of feedback processing. |
| 🤝✉️Weekly Automated Requests for New Loads from Partners | Python, SQLite, Google Sheets, Googel API | pandas, numpy, smtplib, asyncio | This project was created to automate weekly requests to partners about the availability of loads that could be of interest to the company's logisticians. The user could specify the company name, the representative's email, the language of communication, as well as customize the text of the message and specify the address from which the request would be sent. All settings were organized in a separate Google Sheets tab, where you could edit the content of the message and select the sender. |
***
# 🐢Data Science PET Projects
### Context:
This section highlights a selection of personal projects focused on data science and analytics, aimed at improving technical skills and providing insights into various industries. These projects showcase a diverse set of tools and methodologies, demonstrating the versatility and understanding of data science applications across a variety of fields.
| Project Link | Area of Analysis | Tools | Libraries | Project Description |
|---|---|---|---|---|
| 🏠📈 [Housing price prediction]() | Housing Market & Price Estimation | Jupyter Notebook, Python | scikit-learn, pandas, numpy, seaborn, matplotlib | This project predicts housing prices using multiple models, including Random Forest, Decision Tree, and Linear Regression. Extensive feature selection and hyperparameter tuning are performed to achieve accurate price estimates for housing properties. |
| 🛒📊 [Superstore E-Sales Perfomance]() | Retail Analytics & Sales Performance Analysis | Tableau | Tableau | This project analyzes e-sales performance for a superstore, focusing on sales trends, customer behavior, and product performance. Visual dashboards provide insights into sales distribution across Canada and product categories. |
| 🏠🔍 [Analyzing Airbnb Data]() | Short-term Rental Market | SQL | SQL | This project analyzes Airbnb listings in Seattle to uncover trends related to seasonal pricing, neighborhood characteristics, and the growth of homestay activities. Data from Airbnb is used to explore listing characteristics, seasonal demand, and growth trends over time. |
***


