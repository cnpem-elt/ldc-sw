clc;
clear all;
close all;

% Initialize necessary packages
initlibscpi;

% Initialize oscilloscope communication
fid_instr.osc = vxi11('10.0.6.77');

% Initialize signal generator communication
fid_instr.gen = vxi11('10.0.6.64');

% Initialize excitation signal parameters
excit_param = struct;

excit_param.npts = 1e6;
excit_param.Voffset = 0;
excit_param.df = 50;
excit_param.type = 'sin';

# Initialize test frequencies list
excit_param.sin_freq = [50 100:100:1000 2000:1000:10000 20000:10000:100000 200000:100000:500000];
excit_param.nharm = 10;
excit_param.navg = 1;

# Configure oscilloscope channels as Input and Output
channel = struct( ...
    'name_instr', {'CHAN1', 'CHAN2'}, ...
    'name', {'Input', 'Output'}, ...
    'derivative', {0 0} ...
    );

% Initialize communication parameters
param = scpiparam;

% Configure offset (expdef[:,1]) and peak-to-peak (expdef[:,2]) current to use
% on excitation signal
Ioffset = 0;                      % [A]
Ipp = 0.1;                        % [A]
expdef = [ Ioffset*50  Ipp*50 ]; % [V]

% Asks for test name
test_name = input('Enter test name: ', 's');
fprintf('\n');

% Initialize frequency response data structure
freqresps = cell(size(expdef,1),1);

% Run frequency response test for each set of offsets and peak-to-peak voltages
for i=1:size(expdef,1)
    excit_param.Voffset = expdef(i,1);
    excit_param.Vpeak2peak = expdef(i,2);
    
    r = freqresp_keysight(fid_instr, channel, excit_param);
    
    % Save results into file
    r.fname = sprintf('%s_Voffset_%dmV_Vpp_%dmV_%s.mat', test_name, round(excit_param.Voffset*1e3),  round(excit_param.Vpeak2peak*1e3), datestr(now, 'yyyy-mm-dd_HH-MM-SS'));
    save(r.fname, 'r', '-v7');
    
    % Plot results
    freqresps{i} = freqresp_analyze_keysight(r,excit_param.type,[1,2]);
end