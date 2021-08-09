# DonatePayApi

_This library is async wrapper for the DonatePay API._

_Official documentation you can see on https://donatepay.ru/page/api (only after authorization)_
___
**Available methods:**
___
`await client.get_user()`

Parameters: None

**return** User class object (id: int, name: str, avatar: str, balance: int, cashout_sum: int)


___
`await client.get_transactions()` 

Parameters:

**limit**	default = 25, minimal 1, max 100;

**before**	The withdrawal will be carried out until the specified transaction ID

**after**	Withdrawal will be carried out after the specified transaction ID

**skip**	How many transactions need skip

**order**	default = DESC, Sort transactions (ASC - Ascending; DESC - Descending) 

**type**	Type of transaction (donation/cashout)

**status**	success/cancel/wait/user

**return** Transaction class object (id: int, what: str, sum: float, to_cash: Optional[str], to_pay: Optional[str], commission: float, status: str, type: str, vars: [Vars class object (user_ip: Optional[str], name: str, comment: str)], comment: str, created_at: datetime.datetime)
___
`await client.set_notification()`

Parameters:

**name**	Donation Sender Name

**sum**	Donation summ

**comment**	Comment

**date**	Date of transaction creation

**notification**	Create a donation notification ("-1" - No; "1" -

**return** String request result status. If ok, then "result": "success"