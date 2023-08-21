import numpy as np
from parameters import *

AOARANGE = np.array([-1.745329252,-1.658062789,-1.570796327,-1.483529864,-1.396263402,-1.308996939,-1.221730476,-1.134464014,-1.047197551,-0.959931089,-0.174532925,-0.157079633,-0.13962634,-0.122173048,-0.104719755,-0.087266463,-0.06981317,-0.052359878,-0.034906585,-0.017453293,0,0.017453293,0.034906585,0.052359878,0.06981317,0.087266463,0.104719755,0.122173048,0.13962634,0.157079633,0.174532925,0.191986218,0.20943951,0.226892803,0.244346095,0.261799388,0.27925268,0.296705973,0.314159265,0.331612558,0.34906585,0.366519143,0.383972435,0.401425728,0.41887902,0.436332313,0.453785606,0.471238898,0.488692191,0.506145483,0.523598776,0.541052068,0.558505361,0.575958653,0.593411946,0.610865238,0.628318531,0.645771823,0.663225116,0.680678408,0.698131701,0.715584993,0.733038286,0.750491578,0.767944871,0.785398163,0.802851456,0.820304748,0.837758041,0.855211333,0.872664626,0.959931089,1.047197551,1.134464014,1.221730476,1.308996939,1.396263402,1.483529864,1.570796327,1.658062789,1.745329252])
CL = np.array([0.15942029,0.096618357,0.009661836,-0.077294686,-0.144927536,-0.217391304,-0.299516908,-0.357487923,-0.434782609,-0.492753623,-0.234509466,-0.204388985,-0.148450947,-0.126936317,-0.096815835,-0.083907057,-0.058089501,-0.027969019,0.023666093,0.075301205,0.118330465,0.182874355,0.238812392,0.303356282,0.376506024,0.432444062,0.496987952,0.55292599,0.613166954,0.673407917,0.729345955,0.776678141,0.836919105,0.875645439,0.922977625,0.983218589,1.021944923,1.07788296,1.129518072,1.172547332,1.219879518,1.275817556,1.318846816,1.396299484,1.44363167,1.486660929,1.512478485,1.589931153,1.620051635,1.667383821,1.688898451,1.710413081,1.740533563,1.762048193,1.813683305,1.850258176,1.886833046,1.929862306,1.972891566,2.007314974,2.063253012,2.093373494,2.106282272,2.136402754,2.151462995,2.149311532,1.146729776,1.133820998,1.133820998,1.09939759,1.082185886,1.019323671,0.8647343,0.724637681,0.589371981,0.45410628,0.299516908,0.140096618,0.004830918,-0.140096618,-0.280193237])
CD = np.array([0.81906226,0.843658724,0.848578017,0.828900846,0.811683321,0.806764028,0.789546503,0.760030746,0.748962337,0.710837817,0.162962963,0.145679012,0.12345679,0.10617284,0.10617284,0.096296296,0.088888889,0.088888889,0.086419753,0.088888889,0.09382716,0.101234568,0.113580247,0.125925926,0.133333333,0.151851852,0.166666667,0.190123457,0.216049383,0.239506173,0.264197531,0.286419753,0.309876543,0.341975309,0.367901235,0.397530864,0.427160494,0.459259259,0.498765432,0.530864198,0.572839506,0.602469136,0.641975309,0.681481481,0.72345679,0.754320988,0.787654321,0.832098765,0.864197531,0.90617284,0.920987654,0.95308642,0.975308642,1.002469136,1.032098765,1.071604938,1.103703704,1.135802469,1.182716049,1.232098765,1.295061728,1.340740741,1.380246914,1.437037037,1.491358025,1.530864198,1.009876543,1.017283951,1.039506173,1.04691358,1.064197531,1.097002306,1.146195234,1.185549577,1.212605688,1.247040738,1.269177556,1.269177556,1.29377402,1.286395081,1.276556495])
CM = np.array([0.031216649,0.013607257,0.000266809,-0.01547492,-0.031216649,-0.046691569,-0.060565635,-0.073372465,-0.085645678,-0.095517609,-0.038247863,-0.036538462,-0.030982906,-0.027564103,-0.023504274,-0.021581197,-0.017307692,-0.014102564,-0.010042735,-0.008333333,-0.006837607,-0.008119658,-0.00982906,-0.006837607,-0.006623932,-0.004059829,-0.002350427,-0.001068376,-0.001068376,0.000641026,0.003205128,0.007478632,0.010683761,0.013461538,0.016452991,0.021153846,0.025854701,0.031410256,0.034401709,0.04017094,0.043376068,0.048931624,0.053632479,0.061111111,0.068589744,0.07542735,0.083119658,0.088888889,0.096367521,0.103846154,0.111324786,0.115811966,0.125854701,0.137820513,0.144017094,0.152564103,0.160042735,0.171794872,0.180769231,0.18974359,0.2,0.208760684,0.216239316,0.223931624,0.227991453,0.22542735,0.019871795,0.018376068,0.018162393,0.018162393,0.016452991,0.016275347,0.017609392,0.021611526,0.021611526,0.020010672,0.015741729,0.008271078,0.002401281,-0.007203842,-0.011472785])

def getCl(aoa):
    return np.interp(aoa, AOARANGE, CL)

def getCd(aoa):
    return np.interp(aoa, AOARANGE, CD)

def getCm(aoa):
    return np.interp(aoa, AOARANGE, CM)

def get_position_array():
    position_array = [None] * 100
    start_z = 40
    for index, position in enumerate(position_array):
        position_array[index] = (index*4, index*4, start_z - index/2)
    return position_array

# Transformations

def T_gd(angles):
    phi = angles[0]
    theta = angles[1]
    psi = angles[2]
    return np.array([[np.cos(theta)*np.cos(psi), np.sin(phi)*np.sin(theta)*np.cos(psi) - np.cos(phi)*np.sin(psi), np.cos(phi)*np.sin(theta)*np.cos(psi) + np.sin(phi)*np.sin(psi)],
                   [np.cos(theta)*np.sin(psi), np.sin(phi)*np.sin(theta)*np.sin(psi) + np.cos(phi)*np.cos(psi), np.cos(phi)*np.sin(theta)*np.sin(psi) - np.sin(phi)*np.cos(psi)],
                   [-np.sin(theta),            np.sin(phi)*np.cos(theta),                                       np.cos(phi)*np.cos(theta)                                      ]])

def T_dg(angles):
    phi = angles[0]
    theta = angles[1]
    psi = angles[2]
    return np.array([[np.cos(theta)*np.cos(psi),                                      np.cos(theta)*np.sin(psi),                                      -np.sin(theta)            ],
                    [np.sin(phi)*np.sin(theta)*np.cos(psi) - np.cos(phi)*np.sin(psi), np.sin(phi)*np.sin(theta)*np.sin(psi) + np.cos(phi)*np.cos(psi), np.sin(phi)*np.cos(theta)],
                    [np.cos(phi)*np.sin(theta)*np.cos(psi) + np.sin(phi)*np.sin(psi), np.cos(phi)*np.sin(theta)*np.sin(psi) - np.sin(phi)*np.cos(psi), np.cos(phi)*np.cos(theta)]])

def T_ds(beta):
    return np.array([[np.cos(beta), -np.sin(beta), 0],
                   [np.sin(beta),  np.cos(beta), 0],
                   [0,             0,            1]])

def T_sd(beta):
    return np.array([[np.cos(beta),  np.sin(beta), 0],
                   [-np.sin(beta), np.cos(beta), 0],
                   [0,             0,            1]])

def T_sw(alpha):
    return np.array([[np.cos(alpha), 0, -np.sin(alpha)],
                   [0,             1, 0            ],
                   [np.sin(alpha), 0, np.cos(alpha)]])

def T_ws(alpha):
    return np.array([[np.cos(alpha), 0, np.sin(alpha)],
                   [0,             1, 0            ],
                   [-np.sin(alpha), 0, np.cos(alpha)]])

def transform(data, transformMatrix):
    retval = [0, 0, 0]
    for i in range(3):
        for j in range(3):
            retval[i] += transformMatrix[i][j] * data[j]

def throw(rotation, launch_speed, launch_va, launch_ha, nose, roll): #cw/ccw, m/s, deg, deg, deg, deg
    launch_angle = launch_va*(np.pi/180)
    nose_angle = nose*(np.pi/180)
    roll_angle = roll*(np.pi/180)
    
    interval = 0.05
    step = 0
    max_steps = 200
    vector_array_size = [max_steps + 1, 3]
    scalar_array_size = max_steps + 1
    t = np.zeros(scalar_array_size)

    #Ground coordinate system
    pos_g = np.zeros(vector_array_size)
    vel_g = np.zeros(vector_array_size)
    acl_g = np.zeros(vector_array_size)
    ori_g = np.zeros(vector_array_size)
    rot_g = np.zeros(vector_array_size)
    
    #Disc coordinate system
    acl_d = np.zeros(vector_array_size)
    vel_d = np.zeros(vector_array_size)
    rot_d = np.zeros(vector_array_size)
    
    #Side-slip coordinate system
    acl_s = np.zeros(vector_array_size)
    vel_s = np.zeros(vector_array_size)
    rot_s = np.zeros(vector_array_size)
    beta = np.zeros(scalar_array_size)
    
    #Wind coordinate system
    acl_w = np.zeros(vector_array_size)
    vel_w = np.zeros(vector_array_size)
    alpha = np.zeros(scalar_array_size)
    
    #Aerodynamic forces
    drag = np.zeros(scalar_array_size)
    lift = np.zeros(scalar_array_size)
    mom = np.zeros(scalar_array_size)

    #Disc orientation and velocity
    ori_g[step] = np.array([roll_angle, nose_angle, 0])
    vel_g[step] = np.array([launch_speed*np.cos(launch_angle), 0, launch_speed*np.sin(launch_angle)])
    launch_angle_d = np.matmul(T_gd(ori_g[step]), [0, launch_angle, 0])
    ori_g[step] += launch_angle_d

    rho = 1.18
    g = 9.81
    launch_height = 1.5
    pos_g[step] = np.array([[0, 0, launch_height]]) #double check number of square brackets
    
    mass = 0.175 #kg
    diameter = 0.274 #m
    ixy = 0.00134575
    iz = 0.0017675
    area = np.pi * (0.5 * diameter)**2
    omega = launch_speed * 7.619 * rotation
    weight = g*mass


    while pos_g[step][2] > 0:
        if step >= max_steps:
            break
        repeat = False
        while True:
            #ground to wind
            vel_d[step] = np.matmul(T_gd(ori_g[step]), vel_g[step])
            beta[step] = -np.arctan2(vel_d[step][1], vel_d[step][0])
            vel_s[step] = np.matmul(T_ds(beta[step]), vel_d[step])
            alpha[step] = -np.arctan2(vel_s[step][2], vel_s[step][0])
            vel_w[step] = np.matmul(T_sw(alpha[step]), vel_s[step])

            #gravity loads to wind
            grav_d = np.matmul(T_gd(ori_g[step]), [0, 0, -weight])
            grav_s = np.matmul(T_ds(beta[step]), grav_d)
            grav_w = np.matmul(T_sw(alpha[step]), grav_s)

            #aerodynamic forces on disc
            drag[step] = 0.5*rho*(vel_w[step][0]**2)*area*getCd(alpha[step])
            lift[step] = 0.5*rho*vel_w[step][0]**2*area*getCl(alpha[step])
            mom[step] = 0.5*rho*vel_w[step][0]**2*area*diameter*getCm(alpha[step])

            #body accelerations
            acl_w[step,0] = (-drag[step] + grav_w[0]) / mass
            acl_w[step,2] = (lift[step] + grav_w[2]) / mass
            acl_w[step,1] = grav_w[1] / mass
            rot_s[step,0] = -mom[step]/(omega*(ixy - iz))

            #disc accleration to ground
            acl_s[step] = np.matmul(T_ws(alpha[step]), acl_w[step])
            acl_d[step] = np.matmul(T_sd(beta[step]), acl_s[step])
            acl_g[step] = np.matmul(T_dg(ori_g[step]), acl_d[step])

            #roll rate from zero side-slip to ground
            rot_d[step] = np.matmul(T_sd(beta[step]), rot_s[step])
            rot_g[step] = np.matmul(T_dg(ori_g[step]), rot_d[step])

            if step==0:
                break
            if repeat:
                break

            #average accelerations and rotations rates between current and previous steps
            avg_acl_g = (acl_g[step-1] + acl_g[step])/2
            avg_rot_g = (rot_g[step-1] + rot_g[step])/2

            #new velocity, position, and orientation
            vel_g[step] = vel_g[step-1] + avg_acl_g*interval
            pos_g[step] = pos_g[step-1] + vel_g[step-1]*interval + 0.5*avg_acl_g*interval**2
            ori_g[step] = ori_g[step-1] + avg_rot_g*interval

            repeat = True
        
        #estimate velocity, position, and orientation at next step
        vel_g[step+1] = vel_g[step] + acl_g[step]*interval
        pos_g[step+1] = pos_g[step] + vel_g[step]*interval + 0.5*acl_g[step]*interval**2
        ori_g[step+1] = ori_g[step] + rot_g[step]*interval

        #update
        t[step+1] = t[step] + interval
        step += 1

    for time in pos_g:
        for i in range(3):
            time[i] *= 3.28
    
    return pos_g

def throw_wrapper(parameters):
    return throw(parameters.rotation, parameters.launch_speed, parameters.launch_va, parameters.launch_ha, parameters.nose, parameters.roll)