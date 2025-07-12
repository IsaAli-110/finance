function loadData() {
  fetch("/api/data")
    .then((res) => res.json())
    .then((response) => {
      const data = response.data;
      const tbody = document.getElementById("tabel-data");
      const saldoElemen = document.getElementById("saldo");
      let rows = "";
      let saldo = 0;

      data.forEach((item) => {
        const jumlah = parseInt(item.jumlah);
        if (item.tipe === "pemasukan") saldo += jumlah;
        else saldo -= jumlah;

        rows += `
          <tr>
            <td>${item.tanggal}</td>
            <td>${item.keterangan}</td>
            <td>Rp ${jumlah.toLocaleString()}</td>
            <td>${item.tipe}</td>
          </tr>
        `;
      });

      tbody.innerHTML = rows;
      saldoElemen.innerText = `Rp ${saldo.toLocaleString()}`;
    });
}

document.addEventListener('DOMContentLoaded', () => {
  loadData();

  const form = document.getElementById('form-tambah');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    fetch('/api/tambah', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
      if (res.status === "sukses") {
        form.reset();
        loadData(); // Refresh tabel
      } else {
        alert("Gagal menyimpan data.");
      }
    });
});
})