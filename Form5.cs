using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Clinic
{
    public partial class Form5 : Form
    {
        public Form5()
        {
            InitializeComponent();
        }

        private void Form5_Load(object sender, EventArgs e)
        {
            // TODO: данная строка кода позволяет загрузить данные в таблицу "database1DataSet3.Doctor". При необходимости она может быть перемещена или удалена.
            this.doctorTableAdapter.Fill(this.database1DataSet3.Doctor);
            // TODO: данная строка кода позволяет загрузить данные в таблицу "database1DataSet3.Doctor". При необходимости она может быть перемещена или удалена.
            this.doctorTableAdapter.Fill(this.database1DataSet3.Doctor);
            // TODO: данная строка кода позволяет загрузить данные в таблицу "database1DataSet1.Doctors". При необходимости она может быть перемещена или удалена.

        }
    }
}
