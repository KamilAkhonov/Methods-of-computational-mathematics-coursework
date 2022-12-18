using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Clinic
{
    public partial class Form7 : Form
    {

        SqlConnection sqlConnection;

        public Form7()
        {
            InitializeComponent();
        }

        private async void Form7_Load(object sender, EventArgs e)
        {
            // TODO: данная строка кода позволяет загрузить данные в таблицу "database1DataSet8.Clients". При необходимости она может быть перемещена или удалена.
            this.clientsTableAdapter.Fill(this.database1DataSet8.Clients);
            // TODO: данная строка кода позволяет загрузить данные в таблицу "database1DataSet7.Doctor". При необходимости она может быть перемещена или удалена.
            this.doctorTableAdapter.Fill(this.database1DataSet7.Doctor);
            // TODO: данная строка кода позволяет загрузить данные в таблицу "database1DataSet5.Entry". При необходимости она может быть перемещена или удалена.
            this.entryTableAdapter.Fill(this.database1DataSet5.Entry);



            string ConnectionString = @"Data Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=C:\Users\kamil\Documents\БД\Курсач\Clinic\Database1.mdf;Integrated Security=True";

            sqlConnection = new SqlConnection(ConnectionString);


            await sqlConnection.OpenAsync();


            //dataGridView2.Rows.Add();

        }

        private async void button1_Click(object sender, EventArgs e)
        {
            SqlCommand command = new SqlCommand("DELETE FROM [Entry] WHERE [Id] = @id", sqlConnection);

            command.Parameters.AddWithValue("id", textBox1.Text);

            await command.ExecuteNonQueryAsync();

            MessageBox.Show("Запись успешно удалена", "Состояние", MessageBoxButtons.OK);
            this.Close();
        }

    }
}
