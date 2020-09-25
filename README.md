<p align="center">
  <a href="http://projector.tensorflow.org/">
    <img src="./ml_logo.png" alt="ml_logo" width="200" height="165">
 </a>
</p>

<p>Second step in machine learning is to normalize training data.</p>

<p>First of all we need row data: https://github.com/ochirovaur2/ochirovaur2-get_row_data_for_machine_learning_from_jira_database</p>

<p>To normalize training data we use: lemmatization, reqular expressions and stop words</p>


<p>The result of the script execution is the following data in JSON: </p>
<p></p>
<p>nz_input_tickets is input information </p>
<p>cnames is labels </p>
<code>
{
    "nz_input_tickets": [
        "contract день внести новое сотрудник программу ширяев александр фёдорович п п 9253486 курьер"
    ],
    "cnames": [
        "Доступ пользователя / Создание нового пользователя"
    ]
}
</code>
