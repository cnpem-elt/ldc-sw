clear all;
close all;
clc;

% Define filenames from which data will be loaded
filename = {'ldc_freqresp_test_vout_bnc_Voffset_0mV_Vpp_5000mV_2022-03-16_17-20-35.mat', ... 
            'ldc_freqresp_test_vout_bnc_Voffset_5000mV_Vpp_5000mV_2022-03-16_17-22-29.mat', ...
            'ldc_freqresp_test_vout_bnc_Voffset_-5000mV_Vpp_5000mV_2022-03-16_17-24-24.mat', ...
            'ldc_freqresp_test_voltage1_iib_Voffset_0mV_Vpp_5000mV_2022-03-16_17-33-55.mat', ...
            'ldc_freqresp_test_voltage1_iib_Voffset_5000mV_Vpp_5000mV_2022-03-16_17-35-50.mat', ...
            'ldc_freqresp_test_voltage1_iib_Voffset_-5000mV_Vpp_5000mV_2022-03-16_17-37-46.mat'};

% Define legend texts for each case (first one is always -3 dB line in plot_freqresp)
legends = {'-3 dB', ...
           'LDC Vout, Idc = 0 A', ...
           'LDC Vout, Idc = 50 mA', ...
           'LDC Vout, Idc = -50 mA', ...
           'IIB ADC In, Idc = 0 A', ...
           'IIB ADC In, Idc = 50 mA', ...
           'IIB ADC In, Idc = -50 mA'};

% Initialize frequency responses set
freqresps = cell(size(filename,2),1);

% Calculate frequency response for each case and plot
for i=1:size(freqresps,1)
  
    % Load results
    x = load(filename{i});
    r = x.r;
  
    % Calculate results
    freqresps{i} = freqresp_analyze_keysight(r,'sin',[1,2]);
end

% Plot
plot_freqresp(freqresps,legends);
