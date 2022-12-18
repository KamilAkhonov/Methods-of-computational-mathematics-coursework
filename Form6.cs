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
    public partial class Form6 : Form
    {
       

        public Form6()
        {
            InitializeComponent();
        }

        private async void Form6_Load(object sender, EventArgs e)
        {
            // TODO: данная строка кода позволяет загрузить данные в таблицу "database1DataSet4.Nurse". При необходимости она может быть перемещена или удалена.
            this.nurseTableAdapter.Fill(this.database1DataSet4.Nurse);
            // TODO: данная строка кода позволяет загрузить данные в таблицу "database1DataSet4.Doctor". При необходимости она может быть перемещена или удалена.
            // TODO: данная строка кода позволяет загрузить данные в таблицу "database1DataSet4.Nurse". При необходимости она может быть перемещена или удалена.
            this.nurseTableAdapter.Fill(this.database1DataSet4.Nurse);




        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {


        }
    }
}
