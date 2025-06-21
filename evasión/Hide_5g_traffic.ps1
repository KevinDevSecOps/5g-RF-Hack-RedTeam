# Oculta tráfico 5G como tráfico LTE normal
$NIC = Get-NetAdapter -Name "5G_MODEM"
Set-NetAdapterAdvancedProperty -Name $NIC.Name -DisplayName "NR5G Mode" -DisplayValue "LTE"
