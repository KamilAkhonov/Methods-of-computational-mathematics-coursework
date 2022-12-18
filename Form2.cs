using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;

using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Clinic
{
    public partial class Form2 : Form
    {

        SqlConnection sqlConnection;

        public Form2()
        {
            InitializeComponent();
        }

        private void dateTimePicker1_ValueChanged(object sender, EventArgs e)
        {

        }

        private async void Form2_Load(object sender, EventArgs e)
        {
            // TODO: данная строка кода позволяет загрузить данные в таблицу "database1DataSet2.Doctor". При необходимости она может быть перемещена или удалена.
            this.doctorTableAdapter.Fill(this.database1DataSet2.Doctor);
            // TODO: данная строка кода позволяет загрузить данные в таблицу "database1DataSet11.Doctors". При необходимости она может быть перемещена или удалена.
            string connection_string = @"Data Source = (LocalDB)\MSSQLLocalDB; AttachDbFilename = C:\Users\kamil\Documents\БД\Курсач\Clinic\Database1.mdf; Integrated Security = True";
            sqlConnection = new SqlConnection(connection_string);

            await sqlConnection.OpenAsync();


        }

        private async void button1_Click(object sender, EventArgs e)

        {

            SqlCommand E_event = new SqlCommand("SELECT hours_entry FROM [Entry] WHERE date_entry = @de AND hours_entry = @he AND id_doctor = @idoc", sqlConnection);

            E_event.Parameters.AddWithValue("de", monthCalendar1.SelectionStart);
            E_event.Parameters.AddWithValue("he", numericUpDown1.Value);
            E_event.Parameters.AddWithValue("idoc", comboBox1.SelectedValue);


            var have_event = E_event.ExecuteScalar();

            if (have_event == null)
            {
                SqlCommand command = new SqlCommand("SELECT Id FROM [Clients] WHERE Phone = @phone", sqlConnection);

                SqlCommand com = new SqlCommand("SELECT MAX(Id) FROM [Clients]", sqlConnection);

                command.Parameters.AddWithValue("phone", textBox2.Text);

                var id_client = command.ExecuteScalar();



                if (id_client == null)
                {
                    if (com.ExecuteScalar().ToString() == "")
                    {
                        id_client = 1;
                    }
                    else
                    {
                        id_client = (int)com.ExecuteScalar() + 1;
                    }


                    com = new SqlCommand("INSERT INTO [Entry] (id_doctor, id_client, date_entry, hours_entry, note) VALUES(@idoc, @idcl, @de, @he, @nt)", sqlConnection);

                    com.Parameters.AddWithValue("idcl", id_client);
                    com.Parameters.AddWithValue("idoc", comboBox1.SelectedValue);
                    com.Parameters.AddWithValue("de", monthCalendar1.SelectionStart);
                    com.Parameters.AddWithValue("he", numericUpDown1.Value);
                    com.Parameters.AddWithValue("nt", richTextBox1.Text);

                    command = new SqlCommand("INSERT INTO [Clients] (Name, Phone, Birthday, Snils) VALUES(@name, @phone, @bthday, @snls)", sqlConnection);

                    command.Parameters.AddWithValue("name", textBox1.Text);
                    command.Parameters.AddWithValue("phone", textBox2.Text);
                    command.Parameters.AddWithValue("bthday", monthCalendar2.SelectionStart);
                    command.Parameters.AddWithValue("snls", textBox3.Text);

                }
                else
                {
                    command = new SqlCommand("INSERT INTO [Entry] (id_doctor, id_client, date_entry, hours_entry, note) VALUES(@idoc, @idcl, @de, @he, @nt)", sqlConnection);

                    command.Parameters.AddWithValue("idcl", id_client);
                    command.Parameters.AddWithValue("idoc", comboBox1.SelectedValue);
                    command.Parameters.AddWithValue("de", monthCalendar1.SelectionStart);
                    command.Parameters.AddWithValue("he", numericUpDown1.Value);
                    command.Parameters.AddWithValue("nt", richTextBox1.Text);
                }


                await command.ExecuteNonQueryAsync();
                await com.ExecuteNonQueryAsync();

                MessageBox.Show("Вы успешно записаны", "Состояние", MessageBoxButtons.OK);

                this.Close();
            }
            else
            {
                MessageBox.Show("Вы не можете записаться, это время занято", "Состояние", MessageBoxButtons.OK);
                this.Close();
            }





        }

        private void groupBox2_Enter(object sender, EventArgs e)
        {

        }
    }
}
