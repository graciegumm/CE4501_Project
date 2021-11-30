def month(monthly_factors, AADT_Exit, AADT_Waldron, AADT_I24):
    user_input = input('Enter the date (in form of MM/DD/YYYY): ')
    month = int(user_input[0:2])
    factor = monthly_factors[month-1]
    exit_monthly_volume = int(factor * AADT_Exit)
    i24_monthly_volume = int(factor * AADT_I24)
    waldron_monthly_volume = int(factor * AADT_Waldron)
    volumes = [exit_monthly_volume, waldron_monthly_volume, i24_monthly_volume]
    return volumes
    
def time(monthly_volume):
    average_day = [1.04,1.03,1.02,1.01,1.00,1.00,1.15,1.32,1.24,1.14,1.12,1.14,1.17,1.17,1.20,1.27,1.27,1.25,1.23,1.21,1.10,1.08,1.08,1.05]
    sunday = [1.07, 1.05, 1.04,1.02,1.00,1.00,1.00,1.00,1.00,1.03,1.07,1.10,1.12,1.12,1.11,1.11,1.10,1.09,1.08,1.08,1.07,1.05,1.05,1.03]
    monday = [1.03,1.02,1.02,1.01,1.00,1.00,1.19,1.41,1.30,1.14,1.11,1.13,1.15,1.14,1.18,1.28,1.28,1.26,1.24,1.22,1.08,1.06,1.06,1.04]
    tuesday = [1.02,1.02,1.01,1.01,1.00,1.01,1.24,1.50,1.39,1.21,1.14,1.15,1.17,1.17,1.21,1.34,1.34,1.32,1.29,1.26,1.10,1.08,1.08,1.04]
    wednesday = [1.03,1.02,1.02,1.01,1.00,1.01,1.24,1.49,1.39,1.21,1.14,1.15,1.18,1.17,1.22,1.34,1.33,1.31,1.29,1.26,1.10,1.08,1.06,1.04]
    thursday = [1.03,1.03,1.02,1.01,1.00,1.00,1.23,1.47,1.36,1.19,1.14,1.16,1.19,1.18,1.22,1.35,1.34,1.32,1.29,1.27,1.10,1.09,1.08,1.05]
    friday = [1.04,1.03,1.02,1.01,1.00,1.00,1.18,1.35,1.24,1.16,1.16,1.19,1.22,1.23,1.30,1.35,1.34,1.32,1.29,1.27,1.13,1.12,1.11,1.09]
    saturday = [1.06,1.05,1.03,1.02,1.00,1.00,1.00,1.01,1.03,1.07,1.11,1.13,1.16,1.17,1.17,1.16,1.17,1.16,1.15,1.13,1.11,1.11,1.12,1.09]    
    days = [sunday, monday, tuesday, wednesday, thursday, friday, saturday]
    sums = [sum(sunday), sum(monday), sum(tuesday), sum(wednesday), sum(thursday), sum(friday), sum(saturday)]
    daily_factors = [(sum(sunday)/sum(average_day)), (sum(monday)/sum(average_day)), (sum(tuesday)/sum(average_day)), (sum(wednesday)/sum(average_day)), (sum(thursday)/sum(average_day)), (sum(friday)/sum(average_day)), (sum(saturday)/sum(average_day))]
    day = int(input('Input day of the week:\nWhere 1 = Sunday, 2 = Monday, 3 = Tuesday, 4 = Wednesday, 5 = Thursday, 6 = Friday, 7 = Saturday')) - 1
    day_input = days[day]
    time = int(input('What is the current hour (military time): \nFormatted such that 2AM = "2", 10PM = "22"'))
    time_factor = float(day_input[time])
    
    exit_hourly_volume = int(float(monthly_volume[0]) * float(daily_factors[day])/float(sums[day]) * time_factor)
    waldron_hourly_volume = int(float(monthly_volume[1]) * float(daily_factors[day])/float(sums[day]) * time_factor)
    i24_hourly_volume = int(float(monthly_volume[2]) * float(daily_factors[day])/float(sums[day]) * time_factor)
    
    weekly_vol = (int(monthly_volume[0]) * int(average_day[int(time)])) / (sum(average_day))
    hourly_volumes = [exit_hourly_volume, waldron_hourly_volume, i24_hourly_volume]
    return hourly_volumes

def calculate_feet_clear(hourly_volume):
    i24_volume = int(hourly_volume[2])
    length_veh = 20
    length_semi = 72
    average_length = (length_veh * 0.95) + (length_semi *0.05)
    average_gap = 3
    num_lanes = 4
    feet_hour_queue = int((i24_volume * average_length) + (average_gap * (i24_volume - 1)))/num_lanes
    feet_within_scope = 10040.33
    feet_to_clear = 0
    if feet_hour_queue <= feet_within_scope:
        feet_to_clear += feet_hour_queue
    else:
        feet_to_clear += feet_within_scope
    return feet_to_clear
    
def flush_timing(feet_to_clear, hourly_volume):
    ''' Let's assume a few things. 
    
    First, the collision has resulted in all four lanes of I-24 WB being
    blocked west of Waldron Road. 
    
    Second, the collision results in all vehicles attempting to exit I-24 within the region of interest.
    Specifically, the vehicles stopped before Waldron Rd but after the next exit will attempt to exit. 
    
    Since this exit is on the far right, I would assume a large part of the cars in the far left lane do not 
    try to get over. We will estimate this percentage as 10%. As for the second-left lane, I estimate this to be 45%.
    For the lane adjacent to the far right lane, I estimate this to be 60%. For the far right lane, I estimate this 
    to be 100% (to allow for access to the exit). This comes out to an average of 53.75%.
    
    1. Determine how many miles the stopped vehicles (10040.33 ft)
        done above and now passed to this function as feet_to_clear
    
    '''
    
    #data collected on Friday @ 11am hour in November yields the following
    cycle = 113
    red = 2
    yellow = 2.5
    green_exit_base = 20
    green_waldron_base = 84
    hourly_volumes_base = [255, 1073]
    cycle_volume_exit = 8 #veh/cycle, under normal operating circumstances
    
    
    veh_queue = 4 * feet_to_clear/25.6 #4 accounts for each lane
    queue_to_clear = int(veh_queue * 0.5375) #veh/hr      
    
    exit_volume = int(hourly_volume[0]) + queue_to_clear
    two_approaches = [exit_volume, hourly_volume[1]] #veh/hr
    
    #time lost
    l1 = 2.0 #s/phase
    e = 2.0 #s/phase
    l2 = yellow + red - e
    tli = l1 + l2
    loss_cycle = tli + tli
    
    #Comparing the AADT's for North and South Waldron Road, there is (total=34,065)(SB thru = 0.705)(NB thru = 0.295)
    south_bound = 0.705 * hourly_volume[1]
    north_bound = 0.295 * hourly_volume[1]
    
    #determine ELT for Waldron Rd, where ELT only applies to north-bound
    if south_bound <= 1200:
        ELT = (0.000008 *south_bound * south_bound) + (0.0024 * south_bound) + 1.0048
        if ELT > 15:
            ELT == 15
    elif south_bound > 1200:
        ELT = 15
        
    ERT = 1.18 #no pedestrians, applies only to south-bound
    
    #approximate VLT and VRT, where VLT applies to North-Bound Waldron Rd, VRT applies to South-Bound Waldron Rd.
    #let's approximate that 20% of vehicles passing through this intersection are turning to enter I-24 West-Bound
    
    VLTE = (0.20 * north_bound) * ELT
    VRTE = (0.20 * south_bound) * ERT
    
    north_VEQ = VLTE + (0.8 * north_bound)
    south_VEQ = VRTE + (0.8 * south_bound)
    
    north_VEQL = north_VEQ / 2
    south_VEQL = south_VEQ / 2
    
    #Since the exit approach has no opposing traffic, for simplicity, all movements are counted as through
    exit_VEQ = exit_volume #one lane for most of the approach
    
    #critical volume
    if south_VEQL > north_VEQL:
        vca = south_VEQL
    else:
        vca = north_VEQL
    vcb = exit_VEQ
    
    vc = vca + vcb

    cdes = loss_cycle / (1 - (vc / (1700*0.85)))
    
    if cdes < 60: #setting a reasonable minimum cycle length
        cdes = 60
    
    gtot = cdes - loss_cycle

    ga = int(gtot * (vca/vc))
    gb = int(gtot) - ga
    
    plan_list = [ga, gb, gtot, cdes]
    
    return plan_list
        

def output_plan(plan_list):
    ga = plan_list[0]
    gb = plan_list[1]
    gtot = plan_list[2]
    cdes = plan_list[3]
    
    print('')
    print('For the given date and time, the following Flush Signal Timing Plan will be implemented until queueing disperses.')
    print('')
    print('Total cycle length: {}s'.format(int(cdes)))
    print('')
    print('---------- Movement A ----------')
    print('Waldron road approach will be given green balls in each direction')
    print('with permitted left turns north-bound and permitted right turns south-bound')
    print('to allow for vehicles entering I-24 west-bound.')
    print('Movement green time: {}s'.format(ga))
    print('Movement yellow time: 2.5s')
    print('Movement all-red time: 2.0s')
    print('')
    print('---------- Movement B ----------')
    print('Interstate exit approach will be given the signal to allow for left and right turns onto Waldron Road.')
    print('Movement green time: {}s'.format(gb))
    print('Movement yellow time: 2.5s')
    print('Movement all-red time: 2.0s')
    print('')
    print('The total allocated green time for both movements is {}s out of a {}s cycle length.'.format(int(gtot), int(cdes)))
    
def main():
    # determining variation factors from the inputted time and date
    monthly_factors = [0.84282, 0.87252, 0.98391, 1.01361, 1.03218, 1.09901, 1.12129, 1.07673, 1.02475, 1.02847, 0.97649, 0.92822]
    AADT_Exit = (5716/2) #veh/day in the 1 direction
    AADT_Waldron = (24006) #veh/day per direction
    AADT_I24 = (149161/2) #veh/day per direction
    
    monthly_volume = month(monthly_factors, AADT_Exit, AADT_Waldron, AADT_I24)
    hourly_volume = time(monthly_volume)
    feet_to_clear = calculate_feet_clear(hourly_volume)
    plan_list = flush_timing(feet_to_clear, hourly_volume)
    output_plan(plan_list)
    

if __name__ == '__main__':
    main()
