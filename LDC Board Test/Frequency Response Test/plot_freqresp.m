function r = plot_freqresp(freqresps, legends)

figure(1)

subplot(211)
semilogx([freqresps{1}.f(1) freqresps{1}.f(end)], [-3 -3], 'k--', 'LineWidth', 2);
hold all
for i = 1:size(freqresps,1)
    semilogx(freqresps{i}.f, 20*log10(abs(freqresps{i}.fresp)),'LineWidth', 2);
end
grid on    
%title(strrep(test_name,'_','\_'));
title('LDC frequency response test, Ip-p = 100 mA');
xlim([freqresps{1}.f(1) freqresps{1}.f(end)])
ylim([-120 20]);
ylabel('Magnitude [dB]');
legend(legends,'fontsize',8,'Location','Southwest')

    
subplot(212)
for i = 1:size(freqresps,1)
    semilogx(freqresps{i}.f, 180/pi*unwrap(angle(freqresps{i}.fresp)), 'LineWidth', 2);
    hold all
end
grid on
xlim([freqresps{1}.f(1) freqresps{1}.f(end)])
ylabel('Phase [°]');
xlabel('Frequency [Hz]');
