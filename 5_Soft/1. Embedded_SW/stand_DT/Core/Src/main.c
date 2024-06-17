/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "usb_device.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "usbd_cdc_if.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
// ответ на запрос
uint8_t ID[2]={0xBB, 0x0A};

// ответ на команду включения, что мы не зависли и отвечаем
uint8_t ANTWORT[2]={0xEE, 0x0A};
uint8_t ANTWORT_DT[2]={0xCC, 0x0A};

// входной буфер
uint8_t RxData[1] = {0};

// масссив для формирования выхода
uint32_t out_state[32] = {0};

//struct point center = {0};
//union code n;
void Reset_all_outs(void);
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
// отключение адресных выходов для всех мультиплексоров
void Reset_all_outs(void)
{
	HAL_GPIO_WritePin(SW1_1_GPIO_Port, SW1_1_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW1_2_GPIO_Port, SW1_2_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW1_3_GPIO_Port, SW1_3_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW1_4_GPIO_Port, SW1_4_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW1_5_GPIO_Port, SW1_5_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW1_6_GPIO_Port, SW1_6_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW1_7_GPIO_Port, SW1_7_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW1_8_GPIO_Port, SW1_8_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW2_9_GPIO_Port, SW2_9_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW2_10_GPIO_Port, SW2_10_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW2_11_GPIO_Port, SW2_11_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW2_12_GPIO_Port, SW2_12_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW2_13_GPIO_Port, SW2_13_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW2_14_GPIO_Port, SW2_14_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW2_15_GPIO_Port, SW2_15_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW2_16_GPIO_Port, SW2_16_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW3_17_GPIO_Port, SW3_17_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW3_18_GPIO_Port, SW3_18_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW3_19_GPIO_Port, SW3_19_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW3_20_GPIO_Port, SW3_20_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW3_21_GPIO_Port, SW3_21_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW3_22_GPIO_Port, SW3_22_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW3_23_GPIO_Port, SW3_23_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW3_24_GPIO_Port, SW3_24_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW4_25_GPIO_Port, SW4_25_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW4_26_GPIO_Port, SW4_26_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW4_27_GPIO_Port, SW4_27_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW4_28_GPIO_Port, SW4_28_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW4_29_GPIO_Port, SW4_29_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW4_30_GPIO_Port, SW4_30_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW4_31_GPIO_Port, SW4_31_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(SW4_32_GPIO_Port, SW4_32_Pin, GPIO_PIN_RESET);

	HAL_Delay(100);
};

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USB_DEVICE_Init();
  /* USER CODE BEGIN 2 */
  Reset_all_outs();
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

  	  //обработка запроса
  	  CDC_Receive_FS(RxData, 1);

	  switch(RxData[0])
	  {
		  case 1:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW1_1_GPIO_Port, SW1_1_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 2:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW1_2_GPIO_Port, SW1_2_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 3:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW1_3_GPIO_Port, SW1_3_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 4:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW1_4_GPIO_Port, SW1_4_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 5:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW1_5_GPIO_Port, SW1_5_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 6:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW1_6_GPIO_Port, SW1_6_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 7:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW1_7_GPIO_Port, SW1_7_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 8:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW1_8_GPIO_Port, SW1_8_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 9:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW2_9_GPIO_Port, SW2_9_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 10:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW2_10_GPIO_Port, SW2_10_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 11:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW2_11_GPIO_Port, SW2_11_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 12:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW2_12_GPIO_Port, SW2_12_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 13:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW2_13_GPIO_Port, SW2_13_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 14:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW2_14_GPIO_Port, SW2_14_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 15:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW2_15_GPIO_Port, SW2_15_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 16:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW2_16_GPIO_Port, SW2_16_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 17:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW3_17_GPIO_Port, SW3_17_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 18:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW3_18_GPIO_Port, SW3_18_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 19:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW3_19_GPIO_Port, SW3_19_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 20:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW3_20_GPIO_Port, SW3_20_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 21:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW3_21_GPIO_Port, SW3_21_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 22:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW3_22_GPIO_Port, SW3_22_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 23:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW3_23_GPIO_Port, SW3_23_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 24:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW3_24_GPIO_Port, SW3_24_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 25:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW4_25_GPIO_Port, SW4_25_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 26:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW4_26_GPIO_Port, SW4_26_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 27:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW4_27_GPIO_Port, SW4_27_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 28:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW4_28_GPIO_Port, SW4_28_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 29:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW4_29_GPIO_Port, SW4_29_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 30:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW4_30_GPIO_Port, SW4_30_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 31:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW4_31_GPIO_Port, SW4_31_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;
		  case 32:
			  Reset_all_outs();
	  			HAL_GPIO_WritePin(SW4_32_GPIO_Port, SW4_32_Pin, GPIO_PIN_SET);
	  			CDC_Transmit_FS(ANTWORT_DT, 2);
	  			RxData[0] = 0x00;
			break;

		case 170: //запрос опознания, отвечаем на это 0xBB
			CDC_Transmit_FS(ID, 2);
			RxData[0] = 0x00;
			break;
		case 0xFF: //команда полной остановки
			Reset_all_outs();
			CDC_Transmit_FS(ANTWORT, 2);
			RxData[0] = 0x00;
			break;
		default:
			;
			break;
	  }
  	  HAL_Delay(10);

  /*

  HAL_Delay(100);
  HAL_GPIO_TogglePin(E_U_MUX_GPIO_Port, E_U_MUX_Pin);
  CDC_Receive_FS(RxData,  (uint32_t)1);
  CDC_Transmit_FS(ANTWORT, 1);*/

  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE3);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 7;
  RCC_OscInitStruct.PLL.PLLN = 96;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV6;
  RCC_OscInitStruct.PLL.PLLQ = 4;
  RCC_OscInitStruct.PLL.PLLR = 2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV2;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
