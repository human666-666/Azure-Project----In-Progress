# Azure-Project----In-Progress
Azure project (in progress)

## Confirming that the loading was successful
<img width="1895" height="976" alt="police_db" src="https://github.com/user-attachments/assets/e7f94582-7f2a-4d52-8487-bb0f4d8f832b" />

## First query: checking the row count
<img width="370" height="300" alt="1st-query" src="https://github.com/user-attachments/assets/21e97729-852f-4d79-a373-59315b128706" />

## Checking data types
<img width="250" height="300" alt="data-types" src="https://github.com/user-attachments/assets/b4a2a101-55bd-4f21-8819-875841f2204a" />

## Checking character lengths
<img width="1697" height="405" alt="checking-number-of-characters" src="https://github.com/user-attachments/assets/a34a57be-0235-4b8e-956e-4224ebdc1bf4" />

## Creating the clean table
<img width="743" height="502" alt="updated-clean-table-creation" src="https://github.com/user-attachments/assets/081c49a9-b35f-4a53-a4e6-bf180c56f6f8" />

* Made the column names lowercase & used snake case.
* Enforced character limits based on the check I performed in the previous step. The table is static, hence my choice of these character limits.
* The context column was empty, so I removed it. This is appropriate because my table is static & won't be updated
* Created a surrogate key
  
### Confirming
<img width="562" height="327" alt="PK" src="https://github.com/user-attachments/assets/86519e02-e05d-4b37-bb85-27aa9983a11d" />

## Insertion
<img width="905" height="473" alt="insert-pt1" src="https://github.com/user-attachments/assets/3901cb7a-828d-4bcc-b43c-3b487714f975" />
<img width="900" height="407" alt="insert-pt2" src="https://github.com/user-attachments/assets/7231e157-65d5-4ce0-a216-12291e4ec8c9" />
<img width="431" height="192" alt="image" src="https://github.com/user-attachments/assets/e93f4730-68f9-4ede-905d-479247928015" />

### Confirming insertion
<img width="1133" height="323" alt="image" src="https://github.com/user-attachments/assets/5b775f23-f972-4e50-88b8-b2f388a15a72" />
<img width="885" height="257" alt="image" src="https://github.com/user-attachments/assets/117b6edb-6a22-4a03-9ec4-565d4b3fa6c7" />

## Does the constraint work?
<img width="1283" height="431" alt="image" src="https://github.com/user-attachments/assets/2ecacf57-10e9-4880-9320-4a3427048cdc" />

* Yes it does!

## Adding indexes to improve query performance
<img width="520" height="68" alt="image" src="https://github.com/user-attachments/assets/79604656-8bd6-474a-b4ac-e4b0f79b86ad" />
<img width="521" height="57" alt="image" src="https://github.com/user-attachments/assets/327c794a-6ca9-4974-8711-33783bbe38f2" />

## Analytics
<img width="818" height="647" alt="image" src="https://github.com/user-attachments/assets/7729d189-7299-4c18-b65e-aa799b735391" />
<img width="1001" height="666" alt="image" src="https://github.com/user-attachments/assets/37cf23c6-a0be-4c4e-94f1-397fe32ca8eb" />

## Views
<img width="512" height="172" alt="image" src="https://github.com/user-attachments/assets/7ccae6dc-3e1e-402b-b53c-ad740aa20b70" />
<img width="532" height="172" alt="image" src="https://github.com/user-attachments/assets/315d35c5-3bd6-4847-8105-a2e8d84293b9" />

