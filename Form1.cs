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
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Form dlg1 = new Form3();
            dlg1.ShowDialog();
        }

        private void оКлиникеToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Form dlg2 = new Form4();
            dlg2.ShowDialog();
        }

        private void врачиToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Form dlg3 = new Form5();
            dlg3.ShowDialog();
        }

        private void просмотретьToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Form dlg4 = new Form6();
            dlg4.ShowDialog();
        }

        private void расходныеМатериалыToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Form dlg5 = new Form8();
            dlg5.ShowDialog();
        }

        private void записиToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Form dlg6 = new Form7();
            dlg6.ShowDialog();
        }
    }
}
