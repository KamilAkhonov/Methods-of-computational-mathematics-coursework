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
    public partial class Form8 : Form
    {

        SqlConnection sqlConnection;


        public Form8()
        {
            InitializeComponent();
        }

        private async void Form8_Load(object sender, EventArgs e)
        {
            this.materialTableAdapter.Update(this.database1DataSet6.Material);
            // TODO: данная строка кода позволяет загрузить данные в таблицу "database1DataSet6.Material". При необходимости она может быть перемещена или удалена.
            this.materialTableAdapter.Fill(this.database1DataSet6.Material);

            string ConnectionString = @"Data Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=C:\Users\kamil\Documents\БД\Курсач\Clinic\Database1.mdf;Integrated Security=True";

            sqlConnection = new SqlConnection(ConnectionString);


            await sqlConnection.OpenAsync();




        }

        private async void button1_Click(object sender, EventArgs e)
        {
            SqlCommand command = new SqlCommand("INSERT INTO [Material] (Name, Count, Expir_date) VALUES (@Name, @Count, @Exdate)", sqlConnection);

            command.Parameters.AddWithValue("Name", textBox1.Text);
            command.Parameters.AddWithValue("Count", textBox2.Text);
            command.Parameters.AddWithValue("Exdate", monthCalendar1.SelectionStart);

            await command.ExecuteNonQueryAsync();


            MessageBox.Show("Товар успешно добавлен", "Состояние", MessageBoxButtons.OK);
            this.Close();
        }

        private async void button2_Click(object sender, EventArgs e)
        {
            SqlCommand command = new SqlCommand("UPDATE [Material] SET [Name] = @Name, [Count] = @Count, [Expir_date] = @Exdate WHERE [Id] = @id", sqlConnection);
            command.Parameters.AddWithValue("Name", textBox6.Text);
            command.Parameters.AddWithValue("Count", textBox5.Text);
            command.Parameters.AddWithValue("Exdate", monthCalendar2.SelectionStart);
            command.Parameters.AddWithValue("id", textBox4.Text);

            await command.ExecuteNonQueryAsync();

            MessageBox.Show("Товар успешно обновлен", "Состояние", MessageBoxButtons.OK);
            this.Close();

        }

        private async void button3_Click(object sender, EventArgs e)
        {
            SqlCommand command = new SqlCommand("DELETE FROM [Material] WHERE [Id] = @id", sqlConnection);

            command.Parameters.AddWithValue("id", textBox3.Text);

            await command.ExecuteNonQueryAsync();

            MessageBox.Show("Товар успешно удален", "Состояние", MessageBoxButtons.OK);
            this.Close();
        }

        private void tabPage2_Click(object sender, EventArgs e)
        {

        }
    }
}
