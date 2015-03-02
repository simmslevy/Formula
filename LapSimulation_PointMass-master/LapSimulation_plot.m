%% Plot Results  

    [~,apex_indices]    = findpeaks(1./lap_data.v_apex);

    figure(1)

    axs1(1) = subplot(2,1,1);
    plot(track.x,lap_data.v_apex,'Color',[0.5 0.5 0.5])
    hold on
    plot(track.x,lap_data.v,'Color',[0 1 0.7])
    plot(track.x(apex_indices),lap_data.v_apex(apex_indices),'o','Color',[0.5 0.5 0.5])
    scatter(track.x(lap_data.v_driving <= lap_data.v_braking & lap_data.v == lap_data.v_driving ),lap_data.v_driving(lap_data.v_driving <= lap_data.v_braking & lap_data.v == lap_data.v_driving),1,[0.3 0 1],'o')
    scatter(track.x(lap_data.v_driving >= lap_data.v_braking & lap_data.v == lap_data.v_braking ),lap_data.v_braking(lap_data.v_driving >= lap_data.v_braking & lap_data.v == lap_data.v_braking),1,[1 0.3 0],'o')
    hold off
    xlabel('Lap Distance (m)')
    ylabel('Speed (m/s)')
    ylim([0 100])
    grid on
    
    axs1(2) = subplot(2,1,2);
    plot(track.x,lap_data.v,'Color',[0.5 0.5 0.5])
    xlabel('Lap Distance (m)')
    ylabel('Speed (m/s)')
    ylim([0 100])
    grid on  
    hold on
    plot(track.x(brake_point_indices),lap_data.v(brake_point_indices),'o','Color',[1 0 0])
    plot(track.x(drive_point_indices),lap_data.v(drive_point_indices),'o','Color',[0 0 1])
    hold off
%     
%     for indplot = 1:(length(drive_point_indices) - 1)
%     plot(track.x(drive_point_indices(indplot):drive_point_indices(indplot+1)),lap_data.v_liftoff_track{indplot},'g')
%     end
%     
%     for indplot = 1:(length(drive_point_indices) - 1)
%     plot(track.x(drive_point_indices(indplot):drive_point_indices(indplot+1)),lap_data.v_recu_track{indplot},'c')
%     end
%     
%     hold off
% 
    linkaxes(axs1, 'x')

 